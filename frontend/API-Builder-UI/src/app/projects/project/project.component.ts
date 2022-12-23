import { Component, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from 'src/app/auth/services/auth.service';
import { User } from 'src/app/profiles/models/user';
import { UserService } from 'src/app/profiles/services/user.service';
import { Project } from '../project';
import { ProjectServiceService } from '../project-service.service';

@Component({
  selector: 'app-project',
  templateUrl: './project.component.html',
  styleUrls: ['./project.component.less']
})
export class ProjectComponent implements OnInit {

  
  userInfo!: User;
  currentUser!: User;
  isLoading!:boolean;
  id!: string;
  pid!: string;
  defultPic!:string;
  project!:Project;
  my_project_form!:FormGroup<any>;
  constructor(
    private userService: UserService,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute,
    private projectService: ProjectServiceService
  ) {
    this.route.params.subscribe((params) => {
      this.id = params['id'];
      this.pid = params['pid'];
    });

    //this.userService.getUser(this.id).subscribe((data) =>this.userInfo = data);
    this.authService.getCurrentUser().subscribe((user)=>{
    this.currentUser = user;
    })

    this.projectService.getProject(this.pid).subscribe((data)=>{
      this.project = data as Project;
      console.log(this.project,4343434);
    })
  }

modify()
{

}

  ngOnInit(): void {
  }

}