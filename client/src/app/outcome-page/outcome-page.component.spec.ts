import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OutcomePageComponent } from './outcome-page.component';

describe('OutcomePageComponent', () => {
  let component: OutcomePageComponent;
  let fixture: ComponentFixture<OutcomePageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OutcomePageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OutcomePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
