import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../auth/services/auth.service';
import { User } from '../profiles/models/user';
import { UserService } from '../profiles/services/user.service';
import { Project } from './project';
import { ProjectServiceService } from './project-service.service';

@Component({
  selector: 'app-projects',
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.less']
})
export class ProjectsComponent implements OnInit {



  
  userInfo!: User;
  currentUser!: User;
  id!: string;
  defultPic!:string;
  projects!:Project[];
  constructor(
    private userService: UserService,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute,
    private projectService: ProjectServiceService
  ) {
    this.route.params.subscribe((params) => {
      this.id = params['id'];
    });

    this.defultPic = 'https://www.pngfind.com/pngs/m/676-6764065_default-profile-picture-transparent-hd-png-download.png';
    this.userService.getUser(this.id).subscribe((data) =>this.userInfo = data);
    this.authService.getCurrentUser().subscribe((user)=>{
    this.currentUser = user;
    this.projectService.getProjects().subscribe((data)=>{
        this.projects = data as Project[];
        this.projects = this.projects.filter((i) => i.owner === this.userInfo.id && i.private === false) ;
      })
    })
  }

  goProject(pid:number){
   // this.projectService.getProject(pid);
    this.router.navigate([`profiles/${this.id}/projects/${pid}`])
  }

  ngOnInit(): void {
  }

}
