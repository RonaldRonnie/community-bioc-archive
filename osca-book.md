# Archive: #osca-book

## 2025-03-31

**Hervé Pagès** (16:20:01) (in thread):
> This line (from the`extract_array()`method for ResidualMatrixSeed objects defined in the***ResidualMatrix***package):
> ```
> resid <- get_matrix2(x2) - get_Q(x2) %*% get_Qty(x2)
> ```
> assumes that`-`is defined between**matrix-like**object`get_matrix2(x2)`and matrix object`get_Q(x2) %*% get_Qty(x2)`. However there's no such guarantee in general, even if the two operands are guaranteed to be conformable. This is why the following fails (`y`being the ResidualMatrix object obtained in my above post):
> ```
> rms <- ResidualMatrixSeed(y)
> extract_array(rms, list(1:2, 1:3))
> # Error in get_matrix2(x2) - get_Q(x2) %*% get_Qty(x2) : 
>   '-' between a DelayedArray object and an array is not supported yet
> ```
> The following change fixes the problem:
> ```
> hpages@XPS15:~/ResidualMatrix$ git diff
> diff --git a/R/seed.R b/R/seed.R
> index 3b5e4ce..356f7be 100644
> --- a/R/seed.R
> +++ b/R/seed.R
> @@ -185,11 +185,11 @@ setMethod("extract_array", "ResidualMatrixSeed", function(x, index) {
>          index <- rev(index)
>      }
>         x2 <- subset_ResidualMatrixSeed(x, index[[1]], index[[2]])
> -    resid <- get_matrix2(x2) - get_Q(x2) %*% get_Qty(x2)
> +    resid <- as.matrix(get_matrix2(x2)) - get_Q(x2) %*% get_Qty(x2)
>      if (was_transposed) {
>          resid <- t(resid)
>      }
> -    as.matrix(resid)
> +    resid
>  })
> ```
> Do you want to report the issue on the***ResidualMatrix***repo on GitHub@Alan O'C?

**Hervé Pagès** (16:20:43) (in thread):
> This line (from the`extract_array()`method for ResidualMatrixSeed objects defined in the***ResidualMatrix***package):
> ```
> resid <- get_matrix2(x2) - get_Q(x2) %*% get_Qty(x2)
> ```
> assumes that`-`is defined between**matrix-like**object`get_matrix2(x2)`and matrix object`get_Q(x2) %*% get_Qty(x2)`. However there's no such guarantee in general, even if the two operands are guaranteed to be conformable. This is why the following fails (`y`being the ResidualMatrix object obtained in my above post):
> ```
> rms <- ResidualMatrixSeed(y)
> extract_array(rms, list(1:2, 1:3))
> # Error in get_matrix2(x2) - get_Q(x2) %*% get_Qty(x2) : 
>   '-' between a DelayedArray object and an array is not supported yet
> ```
> The following change fixes the problem:
> ```
> hpages@XPS15:~/ResidualMatrix$ git diff
> diff --git a/R/seed.R b/R/seed.R
> index 3b5e4ce..356f7be 100644
> --- a/R/seed.R
> +++ b/R/seed.R
> @@ -185,11 +185,11 @@ setMethod("extract_array", "ResidualMatrixSeed", function(x, index) {
>          index <- rev(index)
>      }
>         x2 <- subset_ResidualMatrixSeed(x, index[[1]], index[[2]])
> -    resid <- get_matrix2(x2) - get_Q(x2) %*% get_Qty(x2)
> +    resid <- as.matrix(get_matrix2(x2)) - get_Q(x2) %*% get_Qty(x2)
>      if (was_transposed) {
>          resid <- t(resid)
>      }
> -    as.matrix(resid)
> +    resid
>  })
> ```
> Do you want to report the issue on the***ResidualMatrix***repo on GitHub@Alan O'C?

**Hervé Pagès** (16:21:09) (in thread):
> This line (from the`extract_array()`method for ResidualMatrixSeed objects defined in the***ResidualMatrix***package):
> ```
> resid <- get_matrix2(x2) - get_Q(x2) %*% get_Qty(x2)
> ```
> assumes that`-`is defined between**matrix-like**object`get_matrix2(x2)`and matrix object`get_Q(x2) %*% get_Qty(x2)`. However there's no such guarantee in general, even if the two operands are guaranteed to be conformable. This is why the following fails (`y`being the ResidualMatrix object obtained in my above post):
> ```
> rms <- ResidualMatrixSeed(y)
> extract_array(rms, list(1:2, 1:3))
> # Error in get_matrix2(x2) - get_Q(x2) %*% get_Qty(x2) : 
>   '-' between a DelayedArray object and an array is not supported yet
> ```
> The following change fixes the problem:
> ```
> hpages@XPS15:~/ResidualMatrix$ git diff
> diff --git a/R/seed.R b/R/seed.R
> index 3b5e4ce..356f7be 100644
> --- a/R/seed.R
> +++ b/R/seed.R
> @@ -185,11 +185,11 @@ setMethod("extract_array", "ResidualMatrixSeed", function(x, index) {
>          index <- rev(index)
>      }
>         x2 <- subset_ResidualMatrixSeed(x, index[[1]], index[[2]])
> -    resid <- get_matrix2(x2) - get_Q(x2) %*% get_Qty(x2)
> +    resid <- as.matrix(get_matrix2(x2)) - get_Q(x2) %*% get_Qty(x2)
>      if (was_transposed) {
>          resid <- t(resid)
>      }
> -    as.matrix(resid)
> +    resid
>  })
> ```
> Do you want to report the issue on the***ResidualMatrix***repo on GitHub@Alan O'C?


## 2025-04-02

**Peter Hickey** (23:32:46) (in thread):
> Okay, PR made after getting it to build locally. Pushed to BioC and hopefully the build goes smoothly


## 2025-04-03

**Ludwig Geistlinger** (08:45:52) (in thread):
> Thanks Pete!
