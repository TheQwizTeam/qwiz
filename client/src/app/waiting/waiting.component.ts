import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { QuizService } from '../quiz-service/quiz.service';
import { WsMessage } from '../models/ws-message';

import { Observable, Subject } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import 'rxjs/add/observable/interval';
import { QwizService } from '../qwiz-service/qwiz-service';

@Component({
  selector: 'app-waiting',
  templateUrl: './waiting.component.html',
  styleUrls: ['./waiting.component.css']
})
export class WaitingComponent implements OnInit {

  roomName: string;
  contestantName: string;

  getContestants = Observable.timer(1000, 1000);
  contestants: string[];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private quizService: QuizService,
    private qwizService: QwizService
  )
  {
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.roomName = params['room'];
      this.contestantName = params['handle']
    });

    this.quizService.open({ roomName: this.roomName, username: this.contestantName });
    var message = new WsMessage('new_contestant', this.roomName, this.contestantName);
    
    this.quizService.registerWithRoom(message);
        
    this.getContestants.subscribe(tick => {
      this.contestants = this.quizService.contestants
    });
  }

  canStartGame(): boolean {
    return this.quizService.isReady();
  }

  startGame() {
    var message = new WsMessage('start_game', this.roomName, this.contestantName);
    this.quizService.startGame(message);
  }

  quit() {
    this.quizService.quit();
  }

}
