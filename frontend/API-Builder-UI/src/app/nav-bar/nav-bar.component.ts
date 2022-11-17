import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth/services/auth.service';

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.less']
})
export class NavBarComponent implements OnInit {
  isAuth!: boolean;
  
  constructor(private authService: AuthService) {
    this.authService.isLoggedIn.subscribe((data)=>{
      this.isAuth = data;
    })
  }
  
logout(){
  this.authService.logout();
}

  ngOnInit(): void {
  }
}