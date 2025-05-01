import json
import os
import re
import string
from datetime import datetime
import html # Import the html module for unescaping

# --- Parsing Functions (mostly unchanged but accept maps) ---

def parse_slack_markdown(text, user_map=None, channel_map=None):
    """
    Converts basic Slack mrkdwn formatting to standard Markdown,
    and replaces user/channel IDs if maps are provided.
    """
    if not text:
        return ""
    text = html.unescape(text)

    # --- Link Replacements ---
    def link_replacer(match):
        url = match.group(1)
        text_content = match.group(2).replace('[', '\\[').replace(']', '\\]')
        return f'[{text_content}]({url})'
    text = re.sub(r'<([^\|>@#]+)\|([^>]+)>', link_replacer, text) # Avoid matching mentions
    text = re.sub(r'<(https?://[^\|>]+)>', r'[\1](\1)', text)

    # --- Basic Formatting ---
    text = re.sub(r'(?<!\w)\*(?!\s)(.*?)(?<!\s)\*(?!\w)', r'**\1**', text) # Bold
    text = re.sub(r'(?<!\w)_(?!\s)(.*?)(?<!\s)_(?!\w)', r'*\1*', text)     # Italics
    text = re.sub(r'(?<!\w)~(?! )(.*?)(?<! )~(?!\w)', r'~~\1~~', text)   # Strikethrough

    # --- ID Replacements (if maps provided) ---
    if user_map:
        text = re.sub(r'<@(U[A-Z0-9]+)>',
                      lambda m: f"@{user_map.get(m.group(1), m.group(1))}", text)
    if channel_map:
        def channel_replacer(match):
            channel_id = match.group(1)
            piped_name = match.group(2)
            # Look up channel name, fallback to ID if not found in map or piped name not present
            channel_name = piped_name or channel_map.get(channel_id, channel_id)
            return f"#{channel_name}"
        text = re.sub(r'<#(C[A-Z0-9]+)(?:\|([^>]+))?>', channel_replacer, text)

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
        link_text = (link_text or url).replace('[', '\\[').replace(']', '\\]')
        text_content = f"[{link_text}]({url})"
    elif el_type == 'emoji':
        text_content = f":{sub_element.get('name', '')}:"
    elif el_type == 'user':
        user_id = sub_element.get('user_id', '')
        # Look up user name, fallback to <@ID> format if not found
        user_name = user_map.get(user_id, f'<@{user_id}>') if user_map else f'<@{user_id}>'
        # Ensure the result starts with @, unless it's still the fallback ID format
        text_content = f"@{user_name}" if not user_name.startswith('<@') else user_name
    elif el_type == 'channel':
        channel_id = sub_element.get('channel_id', '')
        # Look up channel name, fallback to <#ID> format if not found
        channel_name = channel_map.get(channel_id, f'<#{channel_id}>') if channel_map else f'<#{channel_id}>'
         # Ensure the result starts with #, unless it's still the fallback ID format
        text_content = f"#{channel_name}" if not channel_name.startswith('<#') else channel_name
    elif el_type == 'broadcast':
        text_content = f"<!{sub_element.get('range', 'channel')}>"
    else:
        text_content = f"[{el_type} content]"

    styled_text = style_prefix + html.unescape(text_content) + style_suffix

    # Final pass for mentions in text elements (safety net)
    if el_type == 'text':
        styled_text = parse_slack_markdown(styled_text, user_map, channel_map)

    return styled_text

def parse_rich_text_block(block_elements, user_map=None, channel_map=None):
    """
    Parses a list of Slack rich_text block elements into Markdown.
    """
    markdown_parts = []
    for element in block_elements:
        el_type = element.get('type')

        if el_type == 'rich_text':
             markdown_parts.append(parse_rich_text_block(element.get('elements', []), user_map, channel_map))
             continue

        if el_type == 'rich_text_section':
            section_parts = [parse_rich_text_element(sub, user_map, channel_map) for sub in element.get('elements', [])]
            markdown_parts.append("".join(section_parts))
        elif el_type == 'rich_text_list':
            list_parts = []
            indent = "  " * element.get('indent', 0)
            list_type = element.get('style', 'bullet')
            start = element.get('start', 1)
            for i, item_element in enumerate(element.get('elements', [])):
                prefix = f"{indent}* " if list_type == 'bullet' else f"{indent}{start + i}. "
                item_text = parse_rich_text_block([item_element], user_map, channel_map)
                list_parts.append(prefix + item_text)
            markdown_parts.append("\n" + "\n".join(list_parts) + "\n")
        elif el_type == 'rich_text_preformatted':
            # Don't replace mentions in code blocks
            code_parts = [parse_rich_text_element(sub, user_map=None, channel_map=None) for sub in element.get('elements', [])]
            markdown_parts.append(f"\n```\n{''.join(code_parts)}\n```\n")
        elif el_type == 'rich_text_quote':
            quote_parts = [parse_rich_text_element(sub, user_map, channel_map) for sub in element.get('elements', [])]
            markdown_parts.append(f"\n> {''.join(quote_parts)}\n")
        else:
            markdown_parts.append(f"\n[Unsupported block type: {el_type}]\n")

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
    if not ts: return []

    user_id = msg.get('user')
    user_name = "Unknown User"
    if user_id and user_map: user_name = user_map.get(user_id, user_id)
    elif user_id: user_name = user_id
    elif 'user_profile' in msg:
        profile = msg.get('user_profile', {})
        user_name = profile.get('real_name') or profile.get('display_name') or profile.get('name') or user_name
    elif 'username' in msg: user_name = msg.get('username') or user_name
    elif msg.get('subtype') in ['channel_join', 'channel_leave', 'channel_topic', 'channel_purpose']: user_name = "System"

    readable_time = convert_slack_ts_to_readable(ts, '%H:%M:%S')

    message_text = ""
    if 'blocks' in msg and isinstance(msg['blocks'], list):
        try:
            message_text = parse_rich_text_block(msg['blocks'], user_map, channel_map)
            if not message_text and msg.get('text'):
                 message_text = parse_slack_markdown(msg.get('text', ''), user_map, channel_map)
        except Exception as e:
             print(f"    Warn: Error parsing blocks for ts {ts}: {e}. Falling back.")
             message_text = parse_slack_markdown(msg.get('text', ''), user_map, channel_map)
    elif 'text' in msg:
        message_text = parse_slack_markdown(msg.get('text', ''), user_map, channel_map)

    subtype = msg.get('subtype')
    if subtype in ['channel_join', 'channel_leave']:
        system_text = message_text or f'{user_name} {"joined" if subtype == "channel_join" else "left"} the channel'
        # Ensure mentions in default text are replaced
        if user_map:
             system_text = re.sub(r'<@(U[A-Z0-9]+)>', lambda m: f"@{user_map.get(m.group(1), m.group(1))}", system_text)
        markdown_lines.append(f"*{readable_time} - {system_text}*")
        return markdown_lines

    attachments_md = []
    if 'attachments' in msg and isinstance(msg['attachments'], list):
        for attachment in msg['attachments']:
             title = html.unescape(attachment.get('title', 'Attachment'))
             url = attachment.get('original_url') or attachment.get('from_url') or attachment.get('title_link')
             service_name = attachment.get('service_name')
             if url:
                 parsed_title = parse_slack_markdown(title, user_map, channel_map)
                 att_md = f"  - Attachment" + (f" ({service_name})" if service_name else "") + f": [{parsed_title}]({url})"
                 attachments_md.append(att_md)

    files_md = []
    if 'files' in msg and isinstance(msg['files'], list):
        for file_info in msg['files']:
            filename = html.unescape(file_info.get('name', 'File'))
            url = file_info.get('permalink') or file_info.get('url_private_download') or file_info.get('url_private')
            file_type = file_info.get('pretty_type', file_info.get('filetype', ''))
            title = html.unescape(file_info.get('title', filename))
            if url:
                 parsed_title = parse_slack_markdown(title, user_map, channel_map)
                 file_md = f"  - File" + (f" ({file_type})" if file_type else "") + f": [{parsed_title}]({url})"
                 files_md.append(file_md)

    author_str = f"**{user_name}**"
    thread_indicator = " (in thread)" if 'thread_ts' in msg and msg['thread_ts'] != msg['ts'] else ""

    markdown_lines.append(f"{author_str} ({readable_time}){thread_indicator}:")
    if message_text:
        # Text should already have mentions replaced by parsers
        quoted_message_text = message_text.replace('\n', '\n> ')
        markdown_lines.append(f"> {quoted_message_text}")
    elif not attachments_md and not files_md:
         markdown_lines.append("> (No message text)")

    if attachments_md: markdown_lines.extend(attachments_md)
    if files_md: markdown_lines.extend(files_md)

    return markdown_lines

# --- Loading Functions ---

def load_user_map(users_filepath):
    """Loads user ID to name mapping from users.json."""
    user_map = {}
    try:
        # Check if the file exists at the specified path
        if not os.path.exists(users_filepath):
             raise FileNotFoundError() # Raise error to be caught below

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
        # Update warning message to reflect looking in export dir
        print(f"Warning: {os.path.basename(users_filepath)} not found in the specified export directory ({os.path.dirname(users_filepath)}). User IDs won't be replaced.")
    except json.JSONDecodeError: print(f"Error: Could not decode JSON from {users_filepath}.")
    except Exception as e: print(f"Error loading user map from {users_filepath}: {e}")
    return user_map

def load_channel_map(channels_filepath):
    """Loads channel ID to name mapping from channels.json."""
    channel_map = {}
    try:
         # Check if the file exists at the specified path
        if not os.path.exists(channels_filepath):
             raise FileNotFoundError() # Raise error to be caught below

        with open(channels_filepath, 'r', encoding='utf-8') as f:
            channels_data = json.load(f)
        if isinstance(channels_data, list):
            for channel in channels_data:
                if channel.get('id') and channel.get('name'):
                    channel_map[channel.get('id')] = channel.get('name')
            print(f"Loaded {len(channel_map)} channels from {channels_filepath}")
        else: print(f"Warning: Expected list in {channels_filepath}, found {type(channels_data)}.")
    except FileNotFoundError:
         # Update warning message to reflect looking in export dir
        print(f"Warning: {os.path.basename(channels_filepath)} not found in the specified export directory ({os.path.dirname(channels_filepath)}). Channel IDs won't be replaced.")
    except json.JSONDecodeError: print(f"Error: Could not decode JSON from {channels_filepath}.")
    except Exception as e: print(f"Error loading channel map from {channels_filepath}: {e}")
    return channel_map

def sanitize_filename(name):
    """Removes or replaces characters invalid for filenames."""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized_name = ''.join(c for c in name if c in valid_chars)
    sanitized_name = sanitized_name.replace(' ', '_')
    sanitized_name = sanitized_name.strip('._')
    return sanitized_name or "unnamed_channel"

# --- Main Processing Logic ---

def process_channel_directory(channel_dir_path, user_map, channel_map):
    """Loads, sorts, and formats messages for a single channel directory."""
    channel_messages = []
    channel_basename = os.path.basename(channel_dir_path)
    print(f"  Reading message files from '{channel_basename}'...")
    try:
        for filename in sorted(os.listdir(channel_dir_path)):
            if re.match(r'\d{4}-\d{2}-\d{2}\.json$', filename):
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

    # Sort messages
    try:
        valid_messages = [m for m in channel_messages if isinstance(m.get('ts'), (str, int, float)) and m.get('ts')]
        invalid_count = len(channel_messages) - len(valid_messages)
        if invalid_count > 0: print(f"    Warn: Skipped {invalid_count} messages in {channel_basename} due to missing/invalid timestamps.")
        valid_messages.sort(key=lambda x: float(x.get('ts')))
        channel_messages = valid_messages
    except Exception as e:
        print(f"    Warning: Could not sort messages for {channel_basename}: {e}. Proceeding unsorted.")

    # Format messages
    final_markdown_lines = []
    current_date_str = None
    for msg in channel_messages:
        ts = msg.get('ts')
        if not ts: continue
        message_date_str = convert_slack_ts_to_readable(ts, '%Y-%m-%d')
        if message_date_str != current_date_str:
            current_date_str = message_date_str
            final_markdown_lines.append(f"\n## {current_date_str}\n")
        formatted_lines = format_message_markdown(msg, user_map, channel_map)
        final_markdown_lines.extend(formatted_lines)
        if msg.get('subtype') not in ['channel_join', 'channel_leave']:
             final_markdown_lines.append("") # Blank line separator

    return final_markdown_lines


# --- Main Execution ---
if __name__ == "__main__":
    export_dir_default = '.'
    output_dir_default = 'markdown_export'

    export_dir = input(f"Enter the path to the main Slack export directory (default: '{export_dir_default}'): ") or export_dir_default
    output_dir = input(f"Enter the directory to save Markdown files (default: '{output_dir_default}'): ") or output_dir_default

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
        users_filepath = os.path.join(export_dir, 'users.json') # Path within export_dir
        user_map = load_user_map(users_filepath)

        channels_filepath = os.path.join(export_dir, 'channels.json') # Path within export_dir
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
                        # Determine filename and title
                        # Use original directory name for title and sanitized version for filename
                        channel_name_for_file = sanitize_filename(item_name)
                        output_md_filename = f"{channel_name_for_file}.md"
                        output_md_path = os.path.join(output_dir, output_md_filename)
                        # Use original directory name for the title inside the file
                        channel_title = f"# Archive: #{item_name}"

                        # Write channel markdown file
                        if channel_markdown_lines: # Only write if there are messages
                            print(f"  Writing {len(channel_markdown_lines)} lines to {output_md_path}...")
                            try:
                                with open(output_md_path, 'w', encoding='utf-8') as f:
                                    f.write(channel_title + "\n") # Add title line
                                    f.write("\n".join(channel_markdown_lines))
                                # Add to list for README generation
                                processed_channels.append((item_name, output_md_filename))
                            except IOError as e:
                                print(f"  Error writing Markdown file {output_md_path}: {e}")
                            except Exception as e:
                                 print(f"  An unexpected error occurred while writing {output_md_path}: {e}")
                        else:
                             print(f"  Skipping writing file for {item_name} as no messages were formatted.")
                    else:
                         print(f"  Skipping channel {item_name} due to processing errors.")

        except FileNotFoundError:
             print(f"Error: Could not list items in directory '{export_dir}'. Please check the path.")
        except Exception as e:
             print(f"An unexpected error occurred while iterating through directories: {e}")


        # --- Generate README.md Index ---
        if processed_channels:
            readme_path = os.path.join(output_dir, "README.md")
            print(f"\nGenerating index file: {readme_path}")
            try:
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write("# Slack Archive Index\n\n")
                    f.write("Channels:\n\n")
                    # Sort channels alphabetically for the index based on original name
                    processed_channels.sort(key=lambda x: x[0].lower())
                    for channel_name, md_filename in processed_channels:
                        # Use relative path for link in README
                        f.write(f"- [#{channel_name}]({md_filename})\n")
                print("Index file generated successfully.")
            except IOError as e:
                print(f"Error writing README.md file: {e}")
            except Exception as e:
                 print(f"An unexpected error occurred while writing README.md: {e}")
        else:
            print("\nNo channels were processed successfully, skipping README.md generation.")

        print("\nProcessing complete.")
