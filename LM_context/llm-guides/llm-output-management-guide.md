# LLM Output Management Guide

**Last Updated:** July 23, 2025
**Purpose:** To establish clear, actionable rules for generating large outputs to prevent platform-side truncation and ensure response completeness.

---

## 1. The Truncation Problem

Due to platform limitations, large responses, especially those containing long code blocks or file diffs, can be truncated. This leads to incomplete and potentially unusable output. This guide provides a strategy to mitigate this risk.

## 2. Core Principle: Completeness Over Speed

The primary goal is to deliver complete and accurate information, even if it requires breaking the response into multiple parts. A complete, chunked response is always better than a single, truncated one.

## 3. Decision Thresholds: When to Use This Guide

This guide **must** be followed when the anticipated output meets any of the following criteria:

- **Code/Diff Length:** The code block or diff is longer than **150 lines**.
- **File Size:** The total response size is anticipated to be larger than **8KB**.
- **Complexity:** The response involves multiple complex file changes that would benefit from being explained and delivered sequentially.

---

## 4. Strategy for Handling Large Outputs

When a planned response is identified as being large (e.g., >150 lines of code/diff or >8KB of text), the following procedure must be followed.

### 3.1. For New Files

Instead of outputting the entire file at once:

1.  **Announce & Summarize:** Announce that the file is large and provide a high-level summary of its purpose and structure.
2.  **Propose Chunking:** State that you will provide the content in numbered parts to avoid truncation.
3.  **Deliver Part 1:** Output the first part of the file.
4.  **Request Continuation:** End the response by asking the user for a prompt to deliver the next part (e.g., "Please let me know when you are ready for Part 2.").
5.  **Repeat & Verify:** Continue delivering chunks until the file is complete. In the final part, add a confirmation message like "This completes the file."

**Example Interaction:**

> **LLM:** I will now create the new file `.../new-large-file.md`. This file is quite large, so I will provide it in two parts to avoid truncation.
>
> **Part 1: Summary and Beginning**
> This file establishes the new data processing pipeline...
>
> ```diff
> --- /dev/null
> +++ b/path/to/new-large-file.md
> @@ -0,0 +1,100 @@
> +# Data Processing Pipeline
> +... (first 100 lines) ...
> ```
>
> Please let me know when you are ready for Part 2.

### 3.2. For Large Diffs

The same principle applies to large modifications of existing files.

1.  **Announce & Summarize:** Announce that the diff is large and summarize the key changes (e.g., "This change refactors the main function and adds three new helper methods.").
2.  **Deliver in Logical Chunks:** Provide the diff in logical, sequential chunks (e.g., one function or class at a time).
3.  **Request Continuation:** Ask the user to confirm before sending the next chunk.

### 4.3. For Large Text Blocks (Non-Code)

For long explanatory text, use the same chunking method.

1.  **Announce & Summarize:** State that the explanation is detailed and will be broken into parts.
2.  **Deliver Part 1:** Provide the first section of the text.
3.  **Request Continuation:** Ask the user to confirm before providing the next section.

## 5. Implementation Rule

This output management strategy is now a core part of the collaboration workflow. It should be applied automatically whenever a large output is anticipated. This rule supersedes any implicit instruction to provide the full response in a single turn if truncation is a risk.