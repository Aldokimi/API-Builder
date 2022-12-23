import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from 'src/app/auth/services/auth.service';
import { User } from '../models/user';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.less'],
})
export class ProfileComponent implements OnInit {
  userInfo!: User;
  currentUser!: User;
  id!: string;
  defultPic!:string;
  constructor(
    private userService: UserService,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.route.params.subscribe((params) => {
      this.id = params['id'];
      console.log(params['id']);
    });
    this.defultPic = 'https://www.pngfind.com/pngs/m/676-6764065_default-profile-picture-transparent-hd-png-download.png';
    this.userService.getUser(this.id).subscribe((data) =>this.userInfo = data);
    this.authService.getCurrentUser().subscribe((user)=>{
      this.currentUser = user;
    })
  }

  editProfile(){
    this.router.navigate(['home']);
  }

  seeProjects(){
    this.router.navigate([`profiles/${this.id}/projects`]);
  }

  ngOnInit(): void {
    

  }
}
