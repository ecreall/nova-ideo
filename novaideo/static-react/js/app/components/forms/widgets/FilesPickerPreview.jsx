import React from 'react';
import DeleteForeverIcon from 'material-ui-icons/DeleteForever';
import CancelIcon from 'material-ui-icons/Cancel';
import InsertDriveFileIcon from 'material-ui-icons/InsertDriveFile';
import Tooltip from 'material-ui/Tooltip';
import { withStyles } from 'material-ui/styles';

const styles = {
  container: {
    display: 'flex',
    padding: '10px 0px 5px 0px',
    alignItems: 'flex-end'
  },
  files: {
    display: 'flex'
  },
  file: {
    display: 'flex',
    position: 'relative',
    marginRight: 15
  },
  image: {
    width: 38,
    height: 48,
    borderRadius: 3,
    borderWidth: 1,
    borderColor: 'rgba(128, 128, 128, 0.5)',
    backgroundColor: 'rgba(0,0, 0)',
    backgroundRepeat: 'no-repeat',
    backgroundAttachment: 'scroll',
    backgroundPositionX: 'center',
    backgroundPositionY: 'center',
    backgroundSize: 'cover',
    borderStyle: 'solid'
  },
  action: {
    position: 'absolute',
    right: -10,
    top: -6,
    color: 'gray',
    height: 20,
    backgroundColor: 'white',
    borderRadius: 10,
    cursor: 'pointer'
  },
  remove: {
    height: 20,
    width: 20
  },
  removeAll: {
    color: 'gray',
    display: 'flex',
    marginBottom: -4,
    cursor: 'pointer'
  },
  icon: {
    height: 41,
    width: 41,
    color: 'gray'
  }
};

class FilesPickerPreview extends React.Component {
  filesRemoveOne = (file) => {
    this.props.getPicker().removeFile(file);
  };

  filesRemoveAll = () => {
    this.props.getPicker().removeFiles();
  };

  render() {
    const { files, classes } = this.props;
    if (files.length === 0) return null;
    return (
      <div className={classes.container}>
        <div className={classes.removeAll}>
          <Tooltip title="Rmove all files" placement="top">
            <DeleteForeverIcon onClick={this.filesRemoveAll} />
          </Tooltip>
        </div>
        <div className={classes.files}>
          {files.map((file) => {
            return (
              <div className={classes.file} key={file.id}>
                {file.preview.type === 'image'
                  ? <div style={{ backgroundImage: `url("${file.preview.url}")` }} className={classes.image} />
                  : <InsertDriveFileIcon />}
                <div className={classes.action}>
                  <Tooltip title="Remove" placement="top">
                    <CancelIcon
                      classes={{
                        root: classes.remove
                      }}
                      onClick={() => {
                        this.filesRemoveOne(file);
                      }}
                    />
                  </Tooltip>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(FilesPickerPreview);