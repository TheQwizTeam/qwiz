import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs/Observable';

import { QuizService } from '../quiz-service/quiz.service';

@Injectable()
export class LoggedInGuard implements CanActivate {

  constructor(
    private router: Router,
    private quizService: QuizService
  ) { }

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean {
    if (!!this.quizService.currentHandle) {
      return true;
    } else {
      this.router.navigate(['landing']);
      return false;
    }
  }
}
