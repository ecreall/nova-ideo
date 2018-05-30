import React from 'react';
import filesize from 'filesize';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import IconButton from '@material-ui/core/IconButton';

import PhotoCameraIcon from '@material-ui/icons/PhotoCamera';
import DeleteIcon from '@material-ui/icons/Delete';

const styles = (theme) => {
  return {
    container: {
      marginBottom: 10
    },
    imgContainer: {
      borderRadius: 6,
      backgroundClip: ' padding-box',
      margin: 0,
      height: 224,
      position: 'relative',
      '&:hover': {
        '& .image-background': {
          display: 'flex'
        }
      }
    },
    img: {
      cursor: 'pointer',
      borderRadius: 6,
      backgroundClip: ' padding-box',
      margin: 0,
      height: 224,
      backgroundSize: '100% 300%,100%,100%,100%',
      transition: 'background-position 150ms ease',
      backgroundRepeat: 'round',
      backgroundPosition: 'center'
    },
    userIcon: {
      fontSize: '50px !important',
      float: 'right',
      color: 'white',
      padding: 5
    },
    noImgContainer: {
      backgroundColor: theme.palette.tertiary.color
    },
    imgBtn: {
      display: 'none',
      flexDirection: 'column',
      position: 'absolute',
      top: 0,
      bottom: 0,
      right: 0,
      left: 0,
      zIndex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      cursor: 'pointer',
      background: 'rgba(0, 0, 0, 0.4)',
      borderRadius: 6,
      border: `solid 3px ${theme.palette.info[500]}`,
      padding: 10,
      textAlign: 'center'
    },
    imageBackgroundActive: {
      display: 'flex'
    },
    icon: {
      color: 'white',
      fontSize: 50
    },
    deleteBtn: {
      position: 'absolute',
      top: 0,
      right: 0,
      color: 'white'
    },
    label: {
      fontWeight: 900,
      margin: '0 0 .25rem',
      display: 'block',
      fontSize: 15
    },
    helper: {
      color: 'white',
      fontSize: 17,
      fontWeight: 'bold'
    }
  };
};

class ImagePicker extends React.Component {
  static defaultProps = {
    onChange: function () {},
    onError: function () {}
  };

  constructor(props, context) {
    super(props, context);
    this.id = 1;
    this.state = {
      image: this.props.value
    };
  }

  componentDidMount() {
    if (this.props.initRef) {
      this.props.initRef(this);
    }
  }

  onChange = (event) => {
    event.preventDefault();
    const filesAdded = event.dataTransfer ? event.dataTransfer.files : event.target.files;
    let image = null;
    if (filesAdded.length > 0) {
      image = filesAdded[0];
      image.id = 'image';
      image.extension = this.fileExtension(image);
      image.sizeReadable = this.fileSizeReadable(image.size);
      image.preview = {
        type: 'image',
        url: window.URL.createObjectURL(image)
      };
    }
    this.setState(
      {
        image: image
      },
      () => {
        this.props.onChange(this.state.image);
      }
    );
  };

  openFileChooser = () => {
    this.inputElement.value = null;
    this.inputElement.click();
  };

  fileExtension = (file) => {
    const extensionSplit = file.name.split('.');
    if (extensionSplit.length > 1) {
      return extensionSplit[extensionSplit.length - 1];
    }
    return 'none';
  };

  fileSizeReadable = (size) => {
    return filesize(size);
  };

  removeFile = (event) => {
    event.stopPropagation();
    this.setState(
      {
        image: null
      },
      () => {
        this.props.onChange(this.state.image);
      }
    );
  };

  render() {
    const { name, label, helper, classes } = this.props;
    const { image } = this.state;
    const inputAttributes = {
      type: 'file',
      accept: 'image/*',
      name: name,
      style: { display: 'none' },
      ref: (element) => {
        this.inputElement = element;
      },
      onChange: this.onChange
    };
    const imgUrl = image && image.preview && image.preview.url;
    return (
      <div className={classes.container}>
        <input {...inputAttributes} />
        {label &&
          <label className={classes.label} htmlFor={name}>
            {label}
          </label>}
        <div className={classNames(classes.imgContainer, { [classes.noImgContainer]: !imgUrl })} onClick={this.openFileChooser}>
          {imgUrl &&
            <div
              className={classes.img}
              style={{
                backgroundImage: `url('${imgUrl}')`
              }}
            />}
          <div className={classNames('image-background', classes.imgBtn, { [classes.imageBackgroundActive]: !imgUrl })}>
            {imgUrl &&
              <IconButton className={classes.deleteBtn} onClick={this.removeFile}>
                <DeleteIcon />
              </IconButton>}
            <PhotoCameraIcon className={classes.icon} />
            {helper &&
              <div className={classes.helper}>
                {helper}
              </div>}
          </div>
        </div>
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(ImagePicker);