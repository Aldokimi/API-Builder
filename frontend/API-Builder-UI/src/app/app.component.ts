import { Component } from '@angular/core'
import { AuthService } from './auth/services/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent {
  title = 'API-Builder-UI';

  constructor(
    private userService: AuthService,
  ) {
   
  }

  // ngOnInit(): void {
   
  //   this.userService.

  // }

}
