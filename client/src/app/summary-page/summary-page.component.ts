import { Component, OnInit } from '@angular/core';
import { QuizService } from '../quiz-service/quiz.service';

@Component({
  selector: 'app-summary-page',
  templateUrl: './summary-page.component.html',
  styleUrls: ['./summary-page.component.css']
})
export class SummaryPageComponent implements OnInit {

  scores;

  constructor(private quizService: QuizService) { }

  ngOnInit() {
    this.scores = this.quizService.getScores();
  }

  startNew() {

  }

}
