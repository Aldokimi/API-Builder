import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth/services/auth.service';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.less']
})
export class MainPageComponent implements OnInit {

  isAuth!: boolean;
  currentUser!: any; 
  newProfile!:string;
  constructor(private authService: AuthService, private router:Router) {
    this.authService.isLoggedIn.subscribe((data)=>{
      this.isAuth = data;
    })

    if(this.isAuth)
    {
    this.authService.getCurrentUser().subscribe(
      user => { this.currentUser =user;
      this.newProfile = `profiles/${this.currentUser.id}/projects/new-project`
      } 
    ) ;
    }
  }

  ngOnInit(): void {
  }

}
