import React from 'react';
import FilesPicker from './FilesPicker';

class FilesPickerPreview extends React.Component {
  constructor(props) {
    super(props);
    this.picker = null;
    this.state = {
      files: []
    };
  }

  onFilesChange = (files) => {
    this.setState(
      {
        files: files
      },
      () => {
        console.log(this.state.files);
      }
    );
  };

  onFilesError = (error) => {
    console.log(`error code ${error.code}: ${error.message}`);
  };

  filesRemoveOne = (file) => {
    this.picker.removeFile(file);
  };

  filesRemoveAll = () => {
    this.picker.removeFiles();
  };

  render() {
    return (
      <div>
        <h1>Example 1 - List</h1>
        <FilesPicker
          ref={(picker) => {
            this.picker = picker;
          }}
          className="files-dropzone-list"
          style={{ height: '100px' }}
          onChange={this.onFilesChange}
          onError={this.onFilesError}
          multiple
          maxFiles={10}
          maxFileSize={10000000}
          minFileSize={0}
          clickable
        >
          Drop files here or click to upload
        </FilesPicker>
        <button onClick={this.filesRemoveAll}>Remove All Files</button>
        {this.state.files.length > 0
          ? <div className="files-list">
            <ul>
              {this.state.files.map((file) => {
                return (
                  <li className="files-list-item" key={file.id}>
                    <div className="files-list-item-preview">
                      {file.preview.type === 'image'
                        ? <img className="files-list-item-preview-image" src={file.preview.url} />
                        : <div className="files-list-item-preview-extension">
                          {file.extension}
                        </div>}
                    </div>
                    <div className="files-list-item-content">
                      <div className="files-list-item-content-item files-list-item-content-item-1">
                        {file.name}
                      </div>
                      <div className="files-list-item-content-item files-list-item-content-item-2">
                        {file.sizeReadable}
                      </div>
                    </div>
                    <div
                      id={file.id}
                      className="files-list-item-remove"
                        onClick={this.filesRemoveOne.bind(this, file)} // eslint-disable-line
                    />
                  </li>
                );
              })}
            </ul>
          </div>
          : null}
      </div>
    );
  }
}

export default FilesPickerPreview;