import {Component, OnInit} from '@angular/core';
import {FormGroup, NgForm} from '@angular/forms';
import {FileUploader} from 'ng2-file-upload/ng2-file-upload';
import {HttpClient} from '@angular/common/http';
import {ResultService} from '../Result.service';
import {ResultsComponent} from '../results/results.component';
import {Router} from '@angular/router';
import {bind} from '@angular/core/src/render3/instructions';
import {allSettled} from 'q';


@Component({
  selector: 'app-select-index',
  templateUrl: './select-index.component.html',
  styleUrls: ['./select-index.component.css']
})

export class SelectIndexComponent implements OnInit {

  rowSelection = 'multiple';
  min_dist = '3' ;
  dist_from_middle = '0.2';
  max_bad_places = '3';
  min_vol = '85';
  file: any;
  show = '';
  new_data: any;
  records = {};
  rowData = [
    // {'project': 'a', 'num_samples': 4},
    // {'project': 'b', 'num_samples': 6}
    ];
  rowStyle = {};
  formData: FormData = new FormData();
  projectsGridApi = null;
  gridColApi = null;
  error_log: any;
  new_project: string;
  new_indexes: number;
  columnDefs = [
    {headerName: '', field: '', checkboxSelection: true, width: 35},
    {headerName: 'Project', field: 'project', width: 200},
    {headerName: 'Number of Samples', field: 'num_samples', width: 172},

  ];

  constructor(private httpClient: HttpClient,
              public resultService: ResultService,
              private router: Router) {

  }

  ngOnInit() {
  }

  onGridReady(params) {
    this.projectsGridApi = params.api;
    this.gridColApi = params.columnApi;
  }

  onAdd() {
    const newItem = {project: this.new_project, num_samples: this.new_indexes};
    this.projectsGridApi.updateRowData({add: [newItem]});
  }
  onClear() {
    this.projectsGridApi.setRowData([]);
    this.new_project = null;
    this.new_indexes = null;
  }
  onRemoveSelected() {
    const selectedData = this.projectsGridApi.getSelectedRows();
    this.projectsGridApi.updateRowData({ remove: selectedData });
  }

  recordes() {
    const record_dict = [];
    if (this.projectsGridApi != null) {
      this.projectsGridApi.forEachNode(function (rowNode) {
        rowNode.data['num_samples'] = +rowNode.data['num_samples'];
        if (rowNode.data['num_samples'] !== undefined && rowNode.data['num_samples'] !== ''
          && typeof(rowNode.data['num_samples']) === 'number' && isNaN(rowNode.data['num_samples']) === false) {
            record_dict.push({'project': rowNode.data['project'], 'samples': rowNode.data['num_samples']});
        }
      });
    }
    return record_dict;
  }

  getSamplesList(records) {
    const samples_list = [];
    for (const item of records) {
      samples_list.push(item.samples);
    }
    return samples_list;
  }

  onImportPlate(event) {
    const fileList: FileList = event.target.files;
    if (fileList.length > 0) {
      const file: File = fileList[0];
      console.log(file.name + ' imported');
      if ((file.name.split('.').pop()) === 'xlsx') {
        this.file = file;
      } else {
        this.file = null;
      }
    } else {
      this.file = null;
    }
  }

  onSubmit(form: NgForm) {
    this.show = 'Loading, Please wait...';
    this.resultService.showRes(false);
    this.resultService.submitResults([{indexes: [], min_volume: 0}]);
    this.records = this.recordes();
    const samples_list = this.getSamplesList(this.records);
    this.formData.set('min_distance', this.min_dist);
    this.formData.set('dist_from_middle', this.dist_from_middle);
    this.formData.set('max_bad_places', this.max_bad_places);
    this.formData.set('min_volume', this.min_vol);
    this.formData.set('file', this.file);
    this.formData.delete('num_indexes');
    for (const num of samples_list) {
      this.formData.append('num_indexes', num);
    }
    this.httpClient.post('/indexelect/register-index-plate/', this.formData)
      .subscribe(
        (data: any) => {
          if (data['data'].length !== 0) {
            // console.log(data['data']);
            this.resultService.submitRecords(this.records);
            this.resultService.submitResults(data['data']);
            this.new_data = data;
            this.error_log = null;
          }
          this.router.navigate(['/results']);
        },
        (error) => {
          console.log(error);
          this.error_log = error['statusText'] + ' --> Please check you\'r values';
        },
      () => {
          this.resultService.showRes(true);
          // this.resultService.submitResults(this.new_data['data']);

          this.show = '';
      }
      );
  }
}


