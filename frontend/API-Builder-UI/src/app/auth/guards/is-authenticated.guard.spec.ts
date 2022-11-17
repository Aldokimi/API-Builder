import { TestBed } from '@angular/core/testing';
import { AppModule } from 'src/app/app.module';
import { AuthService } from '../services/auth.service';

import { IsAuthenticatedGuard } from './is-authenticated.guard';

describe('IsAuthenticatedGuard', () => {
  let guard: IsAuthenticatedGuard;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports:[AppModule],
      providers:[AuthService]
    });
    guard = TestBed.inject(IsAuthenticatedGuard);
  });

  it('should be created', () => {
    expect(guard).toBeTruthy();
  });
});
