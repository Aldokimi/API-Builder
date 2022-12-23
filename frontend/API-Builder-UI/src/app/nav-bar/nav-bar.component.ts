import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth/services/auth.service';
import { User } from '../profiles/models/user';

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.less']
})
export class NavBarComponent implements OnInit {
  isAuth!: boolean;
  currentUser!: any; 
  profileLink!:string;
  constructor(private authService: AuthService, private router:Router) {
    this.authService.isLoggedIn.subscribe((data)=>{
      this.isAuth = data;
    })

    if(this.isAuth)
    {
    this.authService.getCurrentUser().subscribe(
      user => { this.currentUser =user;
      this.profileLink = `profiles/${this.currentUser.id}`
      } 
    ) ;


    
    }
  }
  
logout(){
  this.authService.logout();
}


goOwnProf(){
 this.router.navigate([`profiles/${ this.currentUser.id}`])
}

  ngOnInit(): void {
   
    
  }
}