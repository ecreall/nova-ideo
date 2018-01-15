import React from 'react';

class FilesPicker extends React.Component {
  static defaultProps = {
    onChange: function () {},
    onError: function () {},
    className: 'files-dropzone',
    dropActiveClassName: 'files-dropzone-active',
    accepts: null,
    multiple: true,
    maxFiles: Infinity,
    maxFileSize: Infinity,
    minFileSize: 0,
    name: 'file',
    clickable: true
  };

  constructor(props, context) {
    super(props, context);
    this.id = 1;
    this.state = {
      files: this.props.value || []
    };
  }

  onDrop = (event) => {
    event.preventDefault();
    this.onDragLeave(event);

    // Collect added files, perform checking, cast pseudo-array to Array,
    // then return to method
    let filesAdded = event.dataTransfer ? event.dataTransfer.files : event.target.files;

    // Multiple files dropped when not allowed
    if (this.props.multiple === false && filesAdded.length > 1) {
      filesAdded = [filesAdded[0]];
    }
    const files = [];
    for (let i = 0; i < filesAdded.length; i += 1) {
      const file = filesAdded[i];
      this.id += 1;
      // Assign file an id
      file.id = `files-${this.id}`;

      // Tell file it's own extension
      file.extension = this.fileExtension(file);

      // Tell file it's own readable size
      file.sizeReadable = this.fileSizeReadable(file.size);

      // Add preview, either image or file extension
      if (file.type && this.mimeTypeLeft(file.type) === 'image') {
        file.preview = {
          type: 'image',
          url: window.URL.createObjectURL(file)
        };
      } else {
        file.preview = {
          type: 'file',
          url: window.URL.createObjectURL(file)
        };
      }

      // Check for file max limit
      if (this.state.files.length + files.length >= this.props.maxFiles) {
        this.onError(
          {
            code: 4,
            message: 'maximum file count reached'
          },
          file
        );
        break;
      }

      // If file is acceptable, push or replace
      if (this.fileTypeAcceptable(file) && this.fileSizeAcceptable(file)) {
        files.push(file);
      }
    }
    this.setState(
      {
        files: this.props.multiple === false ? files : [...this.props.value, ...files]
      },
      () => {
        this.props.onChange(this.state.files);
      }
    );
  };

  onDragOver = (event) => {
    event.preventDefault();
    event.stopPropagation();
  };

  onDragEnter = () => {
    const el = this.dropzone;
    el.className += ` ${this.props.dropActiveClassName}`;
  };

  onDragLeave = () => {
    const el = this.dropzone;
    this.dropzone.className = el.className.replace(` ${this.props.dropActiveClassName}`, '');
  };

  openFileChooser = () => {
    this.inputElement.value = null;
    this.inputElement.click();
  };

  fileTypeAcceptable = (file) => {
    const accepts = this.props.accepts;
    if (accepts) {
      if (file.type) {
        const typeLeft = this.mimeTypeLeft(file.type);
        const typeRight = this.mimeTypeRight(file.type);
        for (let i = 0; i < accepts.length; i += 1) {
          const accept = accepts[i];
          const acceptLeft = accept.split('/')[0];
          const acceptRight = accept.split('/')[1];
          if (acceptLeft && acceptRight) {
            if (acceptLeft === typeLeft && acceptRight === '*') {
              return true;
            }
            if (acceptLeft === typeLeft && acceptRight === typeRight) {
              return true;
            }
          }
        }
      }
      this.onError(
        {
          code: 1,
          message: `${file.name} is not a valid file type`
        },
        file
      );
      return false;
    }
    return true;
  };

  fileSizeAcceptable = (file) => {
    if (file.size > this.props.maxFileSize) {
      this.onError(
        {
          code: 2,
          message: `${file.name} is too large`
        },
        file
      );
      return false;
    } else if (file.size < this.props.minFileSize) {
      this.onError(
        {
          code: 3,
          message: `${file.name} is too small`
        },
        file
      );
      return false;
    }
    return true;
  };

  mimeTypeLeft = (mime) => {
    return mime.split('/')[0];
  };

  mimeTypeRight = (mime) => {
    return mime.split('/')[1];
  };

  fileExtension = (file) => {
    const extensionSplit = file.name.split('.');
    if (extensionSplit.length > 1) {
      return extensionSplit[extensionSplit.length - 1];
    }
    return 'none';
  };

  fileSizeReadable = (size) => {
    if (size >= 1000000000) {
      return `${Math.ceil(size / 1000000000)}GB`;
    } else if (size >= 1000000) {
      return `${Math.ceil(size / 1000000)}MB`;
    } else if (size >= 1000) {
      return `${Math.ceil(size / 1000)}kB`;
    }
    return `${Math.ceil(size)}B`;
  };

  onError = (error, file) => {
    this.props.onError.call(this, error, file);
  };

  removeFile = (fileToRemove) => {
    this.setState(
      {
        files: this.props.value.filter((file) => {
          return file.id !== fileToRemove.id;
        })
      },
      () => {
        this.props.onChange(this.state.files);
      }
    );
  };

  removeFiles = () => {
    this.setState(
      {
        files: []
      },
      () => {
        this.props.onChange(this.state.files);
      }
    );
  };

  render() {
    const { accepts, multiple, name, clickable, className, style, children } = this.props;
    const inputAttributes = {
      type: 'file',
      accept: accepts ? accepts.join() : '',
      multiple: multiple,
      name: name,
      style: { display: 'none' },
      ref: (element) => {
        this.inputElement = element;
      },
      onChange: this.onDrop
    };

    return (
      <div>
        <input {...inputAttributes} />
        <div
          className={className}
          onClick={clickable === true ? this.openFileChooser : null}
          onDrop={this.onDrop}
          onDragOver={this.onDragOver}
          onDragEnter={this.onDragEnter}
          onDragLeave={this.onDragLeave}
          ref={(dropzone) => {
            this.dropzone = dropzone;
          }}
          style={style}
        >
          {children}
        </div>
      </div>
    );
  }
}

export default FilesPicker;