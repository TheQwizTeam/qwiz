import { TestBed, inject } from '@angular/core/testing';

import { QuizService } from './quiz.service';

describe('QuizService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [QuizService]
    });
  });

  it('should ...', inject([QuizService], (service: QuizService) => {
    expect(service).toBeTruthy();
  }));
});
