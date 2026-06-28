AI usage file

```Each entry should include the full prompt, the date and time the prompt was issued, the AI tool used to enter the prompt, a synopsis of the result, and any relevant design or code changes affected by the result. ```

| Date and Time | Prompt | Tool | Response Synopsis | Change |
| --- | --- | --- | --- | --- |
| June 26, 2026, 8:34 PM | How do I isolate a cluster when doing k-means and openCV | Claude | Create binary mask that belong to chosen cluster label, told to flatten then multiply by 255 to convert into a binary mask, then reshape it. | <pre><code>mask = np.uint8(labels.flatten() == cluster_num) * 255</code><br><code>mask = mask.reshape(hsv_normalized.shape[:2])</code><br><code>foreground = cv.bitwise_and(normalized_img, normalized_img, mask=mask)</code></pre>