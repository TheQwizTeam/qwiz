import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

declare var ReconnectingWebSocket;

@Injectable()
export class QuizService {

  websocket: WebSocket;
  currentHandle: string;
  currentQuestion: string;
  currentAnswers: string[];
  correctAnswer: string;
  chosenAnswer: string;
  questionNumber: number;
  scores;
  maxQuestions = 6;

  constructor(private router: Router) { }

  /**
   * Check if the websocket is ready to send and receive messages
   */
  isReady(): boolean {
    return !!(this.websocket && this.websocket.readyState === 1);
  }

  open(roomDetails) {
    this.currentHandle = roomDetails.handle;
    const url = 'ws://localhost:8000/quiz/' + roomDetails.roomName + '/' + roomDetails.handle + '/';
    console.log(url);
    this.websocket = new ReconnectingWebSocket(url);
    this.websocket.onopen = () => {
      console.log('websocket opened');
    };
    this.websocket.onmessage = this.handleIncomingMessage();
    this.websocket.onclose = () => {
      console.log('websocket closed');
    };

    setTimeout(() => {
      const connection = {
        type: QuizMessageType.NewRoom,
        handle: roomDetails.handle,
        message: roomDetails.roomName
      } as QuizMessage;
      this.websocket.send(JSON.stringify(connection));
      console.log('sent message', JSON.stringify(connection));
    }, 1000);
  }

  waitToSend(message: QuizMessage) {
    setTimeout(() => {
      if (this.isReady()) {
        this.websocket.send(JSON.stringify(message));
        console.log('sent message', JSON.stringify(message));
      } else {
        this.waitToSend(message);
      }
    }, 1000);
  }

  handleIncomingMessage() {
    return (message) => {
      // console.log(message);
      const messageData: QuizMessage = JSON.parse(message.data);
      console.log('Got new message', messageData);

      switch (messageData.type) {
        case 0:
          console.log('New Room');
          break;
        case 1:
          console.log('Questions');
          this.questionNumber += 1;
          this.currentQuestion = messageData.question_text;
          this.currentAnswers = [
            messageData.correct_answer,
            messageData.incorrect_answer_1,
            messageData.incorrect_answer_2,
            messageData.incorrect_answer_3
          ];
          this.correctAnswer = messageData.correct_answer;
          this.router.navigate(['question']);
          break;
        case 2:
          console.log('Result');
          break;
        case 3:
          console.log('Summary');
          this.scores = messageData.scores.sort((a, b) => {
            // a comes after b
            if (a[1] < b[1]) {
              return 1;
            }
            // a comes before b
            if (a[1] > b[1]) {
              return -1;
            }
            // a and b are equal
            return 0;
          });
          this.router.navigate(['summary']);
          break;
        default:
          console.log('Unknown message type');
      }
    };
  }

  send() {

  }

  sendMessage(message) {
    const websocketMessage = {
      type: QuizMessageType.Message,
      handle: this.currentHandle,
      message: message
    };
    console.log('Sending websocket message ', websocketMessage);
    this.websocket.send(JSON.stringify(websocketMessage));
  }

  getNextQuestion() {
    const websocketMessage: SendQuizMessage = {
      type: this.questionNumber >= this.maxQuestions ? QuizMessageType.Summary : QuizMessageType.Question,
      handle: this.currentHandle,
      message: this.questionNumber as any
    };
    console.log('Sending websocket message ', websocketMessage);
    this.websocket.send(JSON.stringify(websocketMessage));
    if (this.questionNumber >= this.maxQuestions) {
      this.router.navigate(['complete']);
    }
  }

  sendResult() {
    const websocketMessage: SendQuizMessage = {
      type: QuizMessageType.Result,
      handle: this.currentHandle,
      message: this.getAnswerIsCorrect() ? 'correct' : 'incorrect'
    };
    console.log('Sending websocket message ', websocketMessage);
    this.websocket.send(JSON.stringify(websocketMessage));
  }

  startGame() {
    this.questionNumber = 0;
    this.router.navigate(['start']);
  }

  getCurrentQuestion() {
    return this.currentQuestion;
  }

  getAnswers() {
    return this.shuffle(this.currentAnswers);
  }

  chooseAnswer(answer: string) {
    this.chosenAnswer = answer;
    this.sendResult();
    this.router.navigate(['outcome']);
  }

  getChosenAnswer() {
    return this.chosenAnswer;
  }

  getCorrectAnswer() {
    return this.correctAnswer;
  }

  getAnswerIsCorrect() {
    return this.correctAnswer === this.chosenAnswer;
  }

  getScores() {
    return this.scores;
  }

  quit() {
    this.websocket.close();
  }

  // from http://stackoverflow.com/questions/6274339/how-can-i-shuffle-an-array
  shuffle(a) {
    for (let i = a.length; i; i--) {
      let j = Math.floor(Math.random() * i);
      [a[i - 1], a[j]] = [a[j], a[i - 1]];
    }
    return a;
  }

  testSummaryResponse() {
    const websocketMessage = {
      type: QuizMessageType.Result,
      handle: this.currentHandle,
      message: 'correct',
      q_id: 10
    };
    console.log('Sending websocket message ', websocketMessage);
    this.websocket.send(JSON.stringify(websocketMessage));
  }

}

export class SendQuizMessage {
  type: number;
  handle: string;
  message: string;
}

export class QuizMessage {
  type: number;
  q_id: number;
  handle: string;
  message: string;
  correct_answer: string;
  incorrect_answer_1: string;
  incorrect_answer_2: string;
  incorrect_answer_3: string;
  result: boolean;
  users: string[];
  scores;
  question_text: string;
}

export enum QuizMessageType {
  NewRoom,
  Question,
  Result,
  Summary,
  Message
}

export class UserScores {
  scores: any[];
  // the scores are in the format
  // [0] - handle
  // [1] - score
}
