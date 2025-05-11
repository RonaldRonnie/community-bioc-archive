import json
import os
import re
import string
from datetime import datetime
import html # Import the html module for unescaping

# --- Parsing Functions ---

def parse_slack_markdown(text, user_map=None, channel_map=None):
    """
    Converts basic Slack mrkdwn formatting to standard Markdown,
    replaces user/channel IDs, removes 'r ' prefix from potential inline R.
    """
    if not text:
        return ""
    text = html.unescape(text)

    # --- Escape potential fenced divs to prevent Quarto errors ---
    text = text.replace(':::', '\\:\\:\\:')
    # --- Added: Escape R package double colons (e.g., scRNAseq::function) ---
    text = re.sub(r'(\w+)::(\w+)', r'\1\\:\\:\2', text)

    # --- Link Replacements ---
    def link_replacer(match):
        url = match.group(1)
        text_content = match.group(2).replace('[', '\\[').replace(']', '\\]')
        return f'[{text_content}]({url})'
    text = re.sub(r'<([^\|>@#]+)\|([^>]+)>', link_replacer, text)
    text = re.sub(r'<(https?://[^\|>]+)>', r'[\1](\1)', text)

    # --- Basic Formatting ---
    text = re.sub(r'(?<!\w)\*(?!\s)(.*?)(?<!\s)\*(?!\w)', r'**\1**', text)
    text = re.sub(r'(?<!\w)_(?!\s)(.*?)(?<!\s)_(?!\w)', r'*\1*', text)
    text = re.sub(r'(?<!\w)~(?! )(.*?)(?<! )~(?!\w)', r'~~\1~~', text)

    # --- ID Replacements ---
    if user_map:
        text = re.sub(r'<@(U[A-Z0-9]+)>',
                      lambda m: f"@{user_map.get(m.group(1), m.group(1))}", text)
    if channel_map:
        def channel_replacer(match):
            channel_id = match.group(1)
            piped_name = match.group(2)
            channel_name = channel_map.get(channel_id, piped_name or channel_id)
            return f"#{channel_name}"
        text = re.sub(r'<#(C[A-Z0-9]+)(?:\|([^>]+))?>', channel_replacer, text)

    # --- **REVISED:** Remove 'r ' prefix from potential inline code like `r code()` ---
    # This avoids Quarto attempting to parse it as R code.
    # It specifically targets `r` followed by one or more spaces inside single backticks.
    text = re.sub(r'`r\s+(.*?)`', r'`\1`', text)

    # Also handle the specific malformed case found in general.qmd
    text = text.replace('```r', '```')
    # Also handle the specific malformed case found in bioc_git.qmd
    text = text.replace('```{r ', '```{')

    # --- **ADDED:** Additional handling for 'r' or 'R' prefixes ---
    # Log potential R code for debugging
    if '```r' in text or '```{r' in text or '`r' in text or '```R' in text or '```{R' in text or '`R' in text:
        print(f"  Debug: Found potential R code in text: {text[:100]}...")
    # Inline code: Remove r/R prefix with optional spaces
    text = re.sub(r'`[rR]\s*(.*?)`', r'`\1`', text)
    # Code blocks: Convert to plaintext for consistent rendering
    text = re.sub(r'```[rR]\b', r'```plaintext', text)
    # Code blocks with attributes
    text = re.sub(r'```{[rR]\s*', r'```{plaintext ', text)
    # Fix incomplete code block attributes
    text = re.sub(r'```\{[^}]*$', r'```', text)

    # --- END REVISED ---

    return text.strip()

def parse_rich_text_element(sub_element, user_map=None, channel_map=None):
    """
    Parses a single rich text sub-element into Markdown, replacing IDs.
    """
    text_content = ""
    style_prefix = ""
    style_suffix = ""
    el_type = sub_element.get('type')

    if el_type == 'text':
        text_content = sub_element.get('text', '')
        if 'style' in sub_element:
            style = sub_element['style']
            if style.get('bold'): style_prefix += "**"; style_suffix = "**" + style_suffix
            if style.get('italic'): style_prefix += "*"; style_suffix = "*" + style_suffix
            if style.get('strike'): style_prefix += "~~"; style_suffix = "~~" + style_suffix
            if style.get('code'): style_prefix += "`"; style_suffix = "`" + style_suffix
    elif el_type == 'link':
        url = sub_element.get('url', '#')
        link_text = sub_element.get('text')
        if not link_text and 'unsafe' in sub_element:
            link_text = sub_element.get('unsafe', {}).get('text')
        link_text = (link_text or url).replace('[', '\\[').replace(']', '\\]') # Escape brackets
        text_content = f"[{link_text}]({url})"
    elif el_type == 'emoji':
        text_content = f":{sub_element.get('name', '')}:"
    elif el_type == 'user':
        user_id = sub_element.get('user_id', '')
        user_name = user_map.get(user_id, f'<@{user_id}>') if user_map else f'<@{user_id}>'
        text_content = f"@{user_name}" if not user_name.startswith('<@') else user_name
    elif el_type == 'channel':
        channel_id = sub_element.get('channel_id', '')
        channel_name = channel_map.get(channel_id, f'<#{channel_id}>') if channel_map else f'<#{channel_id}>'
        text_content = f"#{channel_name}" if not channel_name.startswith('<#') else channel_name
    elif el_type == 'broadcast':
        text_content = f"<!{sub_element.get('range', 'channel')}>"
    else:
        # Fallback for unknown rich text elements
        text_content = f"[{el_type} content]"

    # Apply styles AFTER getting base text_content
    styled_text = style_prefix + html.unescape(text_content) + style_suffix

    # Final pass for any remaining Slack mrkdwn within text elements
    # This is where the removal of `r ` will happen for styled text like `*`r code`*`
    if el_type == 'text':
        styled_text = parse_slack_markdown(styled_text, user_map, channel_map)

    return styled_text

def parse_rich_text_block(block_elements, user_map=None, channel_map=None):
    """
    Parses a list of Slack rich_text block elements into Markdown.
    Handles nested structures like lists and sections.
    """
    markdown_parts = []
    for element in block_elements:
        el_type = element.get('type')

        # Handle potential nested blocks first
        if el_type == 'rich_text':
             markdown_parts.append(parse_rich_text_block(element.get('elements', []), user_map, channel_map))
             continue # Skip further processing for this wrapper block

        # Process specific block types
        if el_type == 'rich_text_section':
            # Join parsed sub-elements within the section
            section_parts = [parse_rich_text_element(sub, user_map, channel_map) for sub in element.get('elements', [])]
            markdown_parts.append("".join(section_parts))
        elif el_type == 'rich_text_list':
            list_parts = []
            indent = "  " * element.get('indent', 0)
            list_type = element.get('style', 'bullet') # 'bullet' or 'ordered'
            start = element.get('start', 1) # For ordered lists
            for i, item_element in enumerate(element.get('elements', [])):
                # Determine prefix based on list type
                prefix = f"{indent}* " if list_type == 'bullet' else f"{indent}{start + i}. "
                # Recursively parse the content of the list item (might contain sections etc.)
                item_text = parse_rich_text_block([item_element], user_map, channel_map)
                list_parts.append(prefix + item_text)
            # Join list items with newlines, ensure list block has surrounding newlines
            markdown_parts.append("\n" + "\n".join(list_parts) + "\n")
        elif el_type == 'rich_text_preformatted':
            # Code blocks: process elements without replacing user/channel mentions inside
            code_parts = [parse_rich_text_element(sub, user_map=None, channel_map=None) for sub in element.get('elements', [])]
            code_text = ''.join(code_parts)
            # --- **ADDED:** Normalize newlines to preserve formatting ---
            code_text = code_text.replace('\r\n', '\n').replace('\r', '\n')
            # Log code blocks without newlines for debugging
            if '\n' not in code_text:
                print(f"  Warn: Code block lacks newlines: {code_text[:50]}...")
            # Attempt basic language detection (simple first line check)
            lines = code_text.split('\n', 1)
            lang_hint = ""
            if len(lines) > 1 and len(lines[0].strip()) < 20 and re.match(r'^[a-zA-Z0-9+#_-]+$', lines[0].strip()):
                 lang_hint = "{" + lines[0].strip().lower() + "}"
                 code_text = lines[1] # Use text after the hint
            # Format as Quarto code block ```{lang} or ```
            markdown_parts.append(f"\n```{lang_hint or 'plaintext'}\n{code_text.rstrip()}\n```\n")
        elif el_type == 'rich_text_quote':
            # Blockquotes: process elements normally
            quote_parts = [parse_rich_text_element(sub, user_map, channel_map) for sub in element.get('elements', [])]
            # Join parts and prepend markdown quote syntax to each line
            quoted_text = '> ' + ''.join(quote_parts).replace('\n', '\n> ')
            markdown_parts.append(f"\n{quoted_text}\n")
        else:
            # Fallback for unknown block types
            markdown_parts.append(f"\n[Unsupported block type: {el_type}]\n")

    # Join all parts from the block_elements list
    return "".join(markdown_parts).strip()


def convert_slack_ts_to_readable(ts_string, format='%Y-%m-%d %H:%M:%S'):
    """Converts Slack timestamp string to a specified format."""
    try:
        timestamp = float(ts_string)
        dt_object = datetime.fromtimestamp(timestamp)
        return dt_object.strftime(format)
    except (ValueError, TypeError):
        return ts_string

def format_message_markdown(msg, user_map=None, channel_map=None):
    """Formats a single message dictionary into a list of Markdown lines."""
    markdown_lines = []
    ts = msg.get('ts')
    if not ts: return [] # Skip messages without timestamp

    # Determine user name
    user_id = msg.get('user')
    user_name = "Unknown User"
    if user_id and user_map: user_name = user_map.get(user_id, user_id)
    elif user_id: user_name = user_id
    elif 'user_profile' in msg: # Check user_profile if user field is missing
        profile = msg.get('user_profile', {})
        user_name = profile.get('real_name') or profile.get('display_name') or profile.get('name') or user_name
    elif 'username' in msg: # Bots or apps might use username
        user_name = msg.get('username') or user_name
    elif msg.get('subtype') in ['channel_join', 'channel_leave', 'channel_topic', 'channel_purpose', 'channel_name', 'channel_archive', 'channel_unarchive']:
        # Handle system messages specifically if needed, or assign a generic name
        user_name = "System Event"
        # Use 'text' directly for system messages, parsing it for IDs
        system_text_raw = msg.get('text', f"Event: {msg.get('subtype', 'Unknown')}")
        message_text = parse_slack_markdown(system_text_raw, user_map, channel_map)
        readable_time = convert_slack_ts_to_readable(ts, '%H:%M:%S')
        markdown_lines.append(f"*{readable_time} - {message_text}*")
        return markdown_lines # System message formatting done

    # Format regular message text
    readable_time = convert_slack_ts_to_readable(ts, '%H:%M:%S')
    message_text = ""
    if 'blocks' in msg and isinstance(msg['blocks'], list):
        try:
            # Use rich text parser first
            message_text = parse_rich_text_block(msg['blocks'], user_map, channel_map)
            # Fallback to 'text' field if blocks parsed to empty (rare)
            if not message_text and msg.get('text'):
                 message_text = parse_slack_markdown(msg.get('text', ''), user_map, channel_map)
        except Exception as e:
             print(f"    Warn: Error parsing blocks for ts {ts}: {e}. Falling back to text field.")
             message_text = parse_slack_markdown(msg.get('text', ''), user_map, channel_map)
    elif 'text' in msg:
        # Fallback to simple markdown parsing if no blocks
        message_text = parse_slack_markdown(msg.get('text', ''), user_map, channel_map)

    # Process attachments
    attachments_md = []
    if 'attachments' in msg and isinstance(msg['attachments'], list):
        for attachment in msg['attachments']:
             title = html.unescape(attachment.get('title', 'Attachment'))
             url = attachment.get('original_url') or attachment.get('from_url') or attachment.get('title_link')
             service_name = attachment.get('service_name')
             text = attachment.get('text', '') # Get attachment text (pretext, text, etc.)
             if url:
                 parsed_title = parse_slack_markdown(title, user_map, channel_map)
                 att_md = f"  - Attachment" + (f" ({service_name})" if service_name else "") + f": [{parsed_title}]({url})"
                 # Add attachment text if present, quoting it
                 if text:
                    parsed_text = parse_slack_markdown(text, user_map, channel_map)
                    # Quote each line of the attachment text
                    quoted_text = '> ' + parsed_text.replace('\n', '\n> ')
                    att_md += f"\n{quoted_text}"
                 attachments_md.append(att_md)

    # Process files
    files_md = []
    if 'files' in msg and isinstance(msg['files'], list):
        for file_info in msg['files']:
            filename = html.unescape(file_info.get('name', 'File'))
            # Prefer permalink, fallback to private URLs (might expire)
            url = file_info.get('permalink') or file_info.get('url_private_download') or file_info.get('url_private')
            file_type = file_info.get('pretty_type', file_info.get('filetype', ''))
            title = html.unescape(file_info.get('title', filename)) # Use title if available, else filename
            if url:
                 # Parse title for any markdown/mentions
                 parsed_title = parse_slack_markdown(title, user_map, channel_map)
                 file_md = f"  - File" + (f" ({file_type})" if file_type else "") + f": [{parsed_title}]({url})"
                 files_md.append(file_md)

    # Assemble the final markdown lines for the message
    author_str = f"**{user_name}**"
    thread_indicator = " (in thread)" if 'thread_ts' in msg and msg['thread_ts'] != msg['ts'] else ""

    markdown_lines.append(f"{author_str} ({readable_time}){thread_indicator}:")
    if message_text:
        # Quote the entire message text block
        quoted_message_text = '> ' + message_text.replace('\n', '\n> ')
        markdown_lines.append(quoted_message_text)
    # Add attachments and files below the message text (or if no text)
    if attachments_md: markdown_lines.extend(attachments_md)
    if files_md: markdown_lines.extend(files_md)

    # Add a blank line if there was content, for spacing
    if message_text or attachments_md or files_md:
         markdown_lines.append("") # Add visual separation

    return markdown_lines

# --- Loading Functions ---

def load_user_map(users_filepath):
    """Loads user ID to name mapping from users.json."""
    user_map = {}
    try:
        if not os.path.exists(users_filepath):
             raise FileNotFoundError()
        with open(users_filepath, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        if isinstance(users_data, list):
            for user in users_data:
                user_id = user.get('id')
                user_name = user.get('real_name')
                if not user_name and 'profile' in user:
                     profile = user['profile']
                     user_name = profile.get('real_name_normalized', profile.get('real_name')) or \
                                 profile.get('display_name_normalized', profile.get('display_name'))
                if not user_name: user_name = user.get('name')
                if user_id and user_name: user_map[user_id] = user_name
            print(f"Loaded {len(user_map)} users from {users_filepath}")
        else: print(f"Warning: Expected list in {users_filepath}, found {type(users_data)}.")
    except FileNotFoundError:
        print(f"Warning: {os.path.basename(users_filepath)} not found in the specified export directory ({os.path.dirname(users_filepath)}). User IDs won't be replaced.")
    except json.JSONDecodeError: print(f"Error: Could not decode JSON from {users_filepath}.")
    except Exception as e: print(f"Error loading user map from {users_filepath}: {e}")
    return user_map

def load_channel_map(channels_filepath):
    """Loads channel ID to name mapping from channels.json."""
    channel_map = {}
    try:
        if not os.path.exists(channels_filepath):
             raise FileNotFoundError()
        with open(channels_filepath, 'r', encoding='utf-8') as f:
            channels_data = json.load(f)
        if isinstance(channels_data, list):
            for channel in channels_data:
                if channel.get('id') and channel.get('name'):
                    channel_map[channel.get('id')] = channel.get('name')
            print(f"Loaded {len(channel_map)} channels from {channels_filepath}")
        else: print(f"Warning: Expected list in {channels_filepath}, found {type(channels_data)}.")
    except FileNotFoundError:
        print(f"Warning: {os.path.basename(channels_filepath)} not found in the specified export directory ({os.path.dirname(channels_filepath)}). Channel IDs won't be replaced.")
    except json.JSONDecodeError: print(f"Error: Could not decode JSON from {channels_filepath}.")
    except Exception as e: print(f"Error loading channel map from {channels_filepath}: {e}")
    return channel_map

def sanitize_filename(name):
    """Removes or replaces characters invalid for filenames."""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized_name = ''.join(c for c in name if c in valid_chars)
    sanitized_name = sanitized_name.replace(' ', '_')
    # Remove leading/trailing underscores or periods
    sanitized_name = sanitized_name.strip('._')
    # Ensure filename is not empty after sanitization
    return sanitized_name or "unnamed_channel"

# --- Main Processing Logic ---

def process_channel_directory(channel_dir_path, user_map, channel_map):
    """Loads, sorts, and formats messages for a single channel directory."""
    channel_messages = []
    channel_basename = os.path.basename(channel_dir_path)
    print(f"  Reading message files from '{channel_basename}'...")
    try:
        # Ensure files are processed in date order
        filenames = sorted([f for f in os.listdir(channel_dir_path) if re.match(r'\d{4}-\d{2}-\d{2}\.json$', f)])
        for filename in filenames:
            filepath = os.path.join(channel_dir_path, filename)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        messages_data = json.load(f)
                    if isinstance(messages_data, list):
                        channel_messages.extend(messages_data)
                    else:
                        print(f"    Warn: Skipping {filename} in {channel_basename}, expected list, found {type(messages_data)}.")
                except json.JSONDecodeError:
                    print(f"    Error: Could not decode JSON from {filename} in {channel_basename}")
                except Exception as e:
                    print(f"    Error reading file {filename} in {channel_basename}: {e}")
    except FileNotFoundError:
        print(f"    Error: Directory not found: {channel_dir_path}")
        return None # Indicate error
    except Exception as e:
        print(f"    Error listing files in {channel_dir_path}: {e}")
        return None

    if not channel_messages:
        print(f"    No valid message files found in {channel_basename}.")
        return [] # Return empty list, not an error

    # Sort messages by timestamp ('ts' field)
    try:
        # Filter out messages with invalid or missing 'ts' before sorting
        valid_messages = [m for m in channel_messages if m.get('ts') and isinstance(m.get('ts'), (str, int, float))]
        invalid_count = len(channel_messages) - len(valid_messages)
        if invalid_count > 0: print(f"    Warn: Skipped {invalid_count} messages in {channel_basename} due to missing/invalid timestamps.")
        valid_messages.sort(key=lambda x: float(x.get('ts')))
        channel_messages = valid_messages
    except Exception as e:
        print(f"    Warning: Could not sort messages for {channel_basename}: {e}. Proceeding unsorted.")

    # Format messages into Markdown lines
    final_markdown_lines = []
    current_date_str = None
    for msg in channel_messages:
        ts = msg.get('ts')
        if not ts: continue # Should have been filtered, but safety check
        message_date_str = convert_slack_ts_to_readable(ts, '%Y-%m-%d')
        # Add date header when the date changes
        if message_date_str != current_date_str:
            current_date_str = message_date_str
            # Add extra newline before date header if it's not the first one
            if len(final_markdown_lines) > 0: final_markdown_lines.append("")
            final_markdown_lines.append(f"## {current_date_str}") # Markdown H2 for date
            final_markdown_lines.append("") # Add a newline after the date header

        formatted_lines = format_message_markdown(msg, user_map, channel_map)
        final_markdown_lines.extend(formatted_lines)
        # Already adds blank line in format_message_markdown

    return final_markdown_lines


# --- Main Execution ---
if __name__ == "__main__":
    export_dir_default = '.'
    output_dir_default = 'quarto_export' # Default output directory changed

    export_dir = input(f"Enter the path to the main Slack export directory (default: '{export_dir_default}'): ") or export_dir_default
    output_dir = input(f"Enter the directory to save Markdown (.qmd) files (default: '{output_dir_default}'): ") or output_dir_default

    # Resolve to absolute path for clarity in messages
    export_dir = os.path.abspath(export_dir)
    output_dir = os.path.abspath(output_dir)

    if not os.path.isdir(export_dir):
        print(f"Error: Slack export directory '{export_dir}' not found.")
    else:
        # Create output directory if it doesn't exist
        try:
            os.makedirs(output_dir, exist_ok=True)
            print(f"Output will be saved to '{output_dir}'")
        except OSError as e:
            print(f"Error creating output directory '{output_dir}': {e}")
            exit() # Exit if output directory cannot be created

        # --- Load User and Channel Maps from the EXPORT Directory ---
        print(f"\nLooking for users.json and channels.json in the export directory: {export_dir}")
        users_filepath = os.path.join(export_dir, 'users.json')
        user_map = load_user_map(users_filepath)

        channels_filepath = os.path.join(export_dir, 'channels.json')
        channel_map = load_channel_map(channels_filepath)

        # --- Process Each Channel Subdirectory ---
        processed_channels = [] # Store tuples of (channel_name, filename) for README
        print(f"\nProcessing channel directories in '{export_dir}'...")

        try:
            for item_name in sorted(os.listdir(export_dir)):
                item_path = os.path.join(export_dir, item_name)
                # Process only if it's a directory (potential channel)
                if os.path.isdir(item_path):
                    print(f"\nProcessing channel directory: {item_name}")
                    channel_markdown_lines = process_channel_directory(item_path, user_map, channel_map)

                    if channel_markdown_lines is not None: # Check if processing was successful
                        channel_name_for_file = sanitize_filename(item_name)
                        output_filename = f"{channel_name_for_file}.qmd"
                        output_path = os.path.join(output_dir, output_filename)

                        # --- Added: Markdown header ---
                        markdown_header = f"# {item_name}\n"

                        # Write channel md file
                        if channel_markdown_lines: # Only write if there are messages
                            print(f"  Writing {len(channel_markdown_lines)} lines to {output_path}...")
                            try:
                                with open(output_path, 'w', encoding='utf-8') as f:
                                    f.write(markdown_header + "\n") # Write Markdown header
                                    f.write("\n".join(channel_markdown_lines))
                                processed_channels.append((item_name, output_filename))
                            except IOError as e:
                                print(f"  Error writing Markdown file {output_path}: {e}")
                            except Exception as e:
                                 print(f"  An unexpected error occurred while writing {output_path}: {e}")
                        else:
                             print(f"  Skipping writing file for {item_name} as no messages were formatted.")
                    else:
                         print(f"  Skipping channel {item_name} due to processing errors.")

        except FileNotFoundError:
             print(f"Error: Could not list items in directory '{export_dir}'. Please check the path.")
        except Exception as e:
             print(f"An unexpected error occurred while iterating through directories: {e}")

        # --- Generate README.md Index (linking to .qmd) ---
        if processed_channels:
            readme_path = os.path.join(output_dir, "README.md")
            print(f"\nGenerating index file (README.md) linking to .qmd files...")
            try:
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write("# Slack Archive Index\n\n")
                    f.write("Channels:\n\n")
                    processed_channels.sort(key=lambda x: x[0].lower())
                    for channel_name, qmd_filename in processed_channels:
                        f.write(f"- [#{channel_name}]({qmd_filename})\n") # Link uses .qmd
                print("Index file generated successfully.")
            except IOError as e:
                print(f"Error writing README.md file: {e}")
            except Exception as e:
                 print(f"An unexpected error occurred while writing README.md: {e}")
        else:
            print("\nNo channels were processed successfully, skipping README.md generation.")

        print("\nProcessing complete.")
