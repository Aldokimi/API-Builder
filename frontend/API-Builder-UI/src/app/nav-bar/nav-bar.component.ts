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
  myApiLink!:string;
  newApiLink!:string;
  searchTerm = '';
  searchLink!:string
  
  search() {
    this.searchLink=`profiles?search=${this.searchTerm}`;
  }
  
  constructor(private authService: AuthService, private router:Router) {
    this.authService.isLoggedIn.subscribe((data)=>{
      this.isAuth = data;
    })

   // if(this.isAuth)
    {
         
    this.authService.currentUser.subscribe(
      user => { this.currentUser =user;
      this.profileLink = `profiles/${this.currentUser.id}`
      this.myApiLink = `profiles/${this.currentUser.id}/projects`
      this.newApiLink = `profiles/${this.currentUser.id}/projects/new-project`
      } 
    ) ;

    this.authService.getCurrentUser().subscribe(
      user => { this.currentUser =user;
      this.profileLink = `profiles/${this.currentUser.id}`
      this.myApiLink = `profiles/${this.currentUser.id}/projects`
      this.newApiLink = `profiles/${this.currentUser.id}/projects/new-project`
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