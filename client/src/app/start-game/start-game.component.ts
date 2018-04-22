import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { QuizService } from '../quiz-service/quiz.service';
import { WsMessage } from '../models/ws-message';

@Component({
  selector: 'app-start-game',
  templateUrl: './start-game.component.html',
  styleUrls: ['./start-game.component.css']
})
export class StartGameComponent implements OnInit {

  countDown = 3;

  roomName: string;
  contestantName: string;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private quizService: QuizService
  ) {
    this.roomName = 'Room Name';
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.roomName = params['room'];
      this.contestantName = params['handle']
    });

    var message = new WsMessage('start_quiz', this.roomName, this.contestantName);
    this.quizService.startGame(message);

    const interval = setInterval(() => {
      this.countDown -= 1;
      if (this.countDown < 1) {
        clearInterval(interval);
        console.log('starting game');
        this.router.navigate(['question', this.roomName, this.contestantName]);
      }
    }, 1000);
  }

}
