AI usage file

```Each entry should include the full prompt, the date and time the prompt was issued, the AI tool used to enter the prompt, a synopsis of the result, and any relevant design or code changes affected by the result. ```

| Date and Time | Prompt | Tool | Response Synopsis | Change |
| --- | --- | --- | --- | --- |
| June 20th, 2026, 8:25 PM | How would you go about making a sudoku solver that solves from real world pictures? | Gemini | (1) isolate grid from background, (2) pull out individual digits from the grid. (3) use OCR for digit recognitiion. (4) apply a sudoku solver algorithm. (5) Overlay or display solution somehow. | No change, just needed for ideas |
| July 4th, 2026, 7:03 PM | Can you double check my get_lines() function | Claude | Logic was slightly incorrect since logic was flipped on horizontal and vertical lines | Changed logic to what claude noted | 
| July 5th, 2026, 2:29 PM | How can I get rid of little specs of noise in my individual cells <insert picture of cell> | Claude | Use the morphologyEx function from openCV to clean up noise then use connectedComponentsWithStats to pick the biggest component that doesn't touch an edge then create an all black image then add back in the number| Added the isolate_digit function in cells.py |
| July 11th, 2026, 12:31 AM | My mnist cnn is currently misclassifying a lot of digits as 2 what would you suggest be the best way to solve this issue | ChatGPT | Normalize to fit the mnist input in terms of centering and sizing and possibly train a model that focuses on printed digits instead of mnist since mnist is drawn| In process of making function for centering and sizing will update when done|