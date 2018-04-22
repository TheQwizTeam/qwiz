import { TestBed, inject } from '@angular/core/testing';

import { QwizServiceService } from './qwiz-service.service';

describe('QwizServiceService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [QwizServiceService]
    });
  });

  it('should ...', inject([QwizServiceService], (service: QwizServiceService) => {
    expect(service).toBeTruthy();
  }));
});
