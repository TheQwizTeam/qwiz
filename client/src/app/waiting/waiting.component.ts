import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { QuizService } from '../quiz-service/quiz.service';

@Component({
  selector: 'app-waiting',
  templateUrl: './waiting.component.html',
  styleUrls: ['./waiting.component.css']
})
export class WaitingComponent implements OnInit {

  roomName: string;

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
    });
  }

  sendMessage() {
    this.quizService.sendMessage('message');
  }

  canStartGame(): boolean {
    return this.quizService.isReady();
  }

  startGame() {
    this.quizService.startGame();
  }

  quit() {
    this.quizService.quit();
  }

}
