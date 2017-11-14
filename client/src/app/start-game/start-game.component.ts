import { Component, OnInit } from '@angular/core';

import { QuizService } from '../quiz-service/quiz.service';

@Component({
  selector: 'app-start-game',
  templateUrl: './start-game.component.html',
  styleUrls: ['./start-game.component.css']
})
export class StartGameComponent implements OnInit {

  countDown = 3;

  constructor(private quizService: QuizService) { }

  ngOnInit() {
    const interval = setInterval(() => {
      this.countDown -= 1;
      if (this.countDown < 1) {
        clearInterval(interval);
        console.log('starting game');
        this.quizService.getNextQuestion();
      }
    }, 1000);
  }

}
