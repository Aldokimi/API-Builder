import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from 'src/app/auth/services/auth.service';
import { User } from '../models/user';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-profiles',
  templateUrl: './profiles.component.html',
  styleUrls: ['./profiles.component.less']
})
export class ProfilesComponent implements OnInit {
  filteredUsers!:User[]
  allUsers!:User[]
  searchTerm!:string
  constructor(private route: ActivatedRoute,private authservice:AuthService,private userService:UserService,private router:Router  ){ 

    this.route.queryParams.subscribe(params => {
      this.searchTerm = params['search']
    });
    
  }

  ngOnInit(): void {
    this.userService.getAllUsers().subscribe(
      (users)=>{
        
        this.allUsers = users as User[];
        this.filteredUsers = this.allUsers.filter((user) => {
          return user.username.toLowerCase().includes(this.searchTerm.toLowerCase());
        });
      }
    )
  }

viewprofile(id:number){
  this.router.navigate([`profiles/${id}`])
}

}
