import { Component, OnInit } from '@angular/core';
import { ProjectServiceService } from './project-service.service';

@Component({
  selector: 'app-projects',
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.less']
})
export class ProjectsComponent implements OnInit {

  constructor(private projectService: ProjectServiceService) { }

  ngOnInit(): void {
  }

}
