# Message types

### Request a room from server

This message will create a room on the server if it doesn't exist and add the user to the room.

| JSON key | meaning |
|----------|---------|
| type | 0 - Room |
| handle | user handle |
| message | room name |

### Receive a new question from the server

This message will set the question on the client for the user to answer.

| JSON key | meaning |
|----------|---------|
| type | 1 - Question |
| question_text | question |
| incorrect_answer_1 | incorrect answer #1 |
| incorrect_answer_2 | incorrect answer #2 |
| incorrect_answer_3 | incorrect answer #3 |
| correct_answer | correct answer |

### Send result

This message will inform the server if the user chose the correct or incorrect answer, the server will then adjust the score accordingly.

| JSON key | meaning |
|----------|---------|
| type | 2 - Result |
| handle | user handle |
| message | string either 'correct' or 'incorrect' |

### Request summary

This message tells the server that the user has finished answering questions, and requests the summary. If all users have finished then the server will push the summary.

| JSON key | meaning |
|----------|---------|
| type | 3 - Summary |
| handle | the handle of the current user |
| message | the question number (not used) |

### Receive summary

This message contains a list of the scores from the server to display to the user.

| JSON key | meaning |
|----------|---------|
| type | 3 - Summary |
| scores | An array of tuples containing the handle and score of each user |
