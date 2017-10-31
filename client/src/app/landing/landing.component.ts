import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';

import { QuizService } from '../quiz-service/quiz.service';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css']
})
export class LandingComponent implements OnInit {

  roomForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private quizService: QuizService
  ) {
    this.roomForm = this.fb.group({
      joinCode: this.fb.control(''),
      handle: this.fb.control('')
    });
  }

  ngOnInit() {
  }

  joinroom(formValue) {
    console.log("Joining :" + formValue);
    this.quizService.open(formValue);
    this.router.navigate(['waiting', formValue.joinCode, formValue.handle]);
  }

  newroom() {
    console.log("New Room");
    this.router.navigate(['newroom']);
  }

}
