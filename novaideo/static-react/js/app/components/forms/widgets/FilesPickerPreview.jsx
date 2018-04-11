import React from 'react';
// import DeleteForeverIcon from 'material-ui-icons/DeleteForever';
import CancelIcon from 'material-ui-icons/Cancel';
import classNames from 'classnames';
import Icon from 'material-ui/Icon';
import Tooltip from 'material-ui/Tooltip';
import { withStyles } from 'material-ui/styles';
import { I18n } from 'react-redux-i18n';

import { FILES_ICONS } from '../../../constants';
import { getFileType } from '../../../utils/globalFunctions';

const styles = {
  container: {
    display: 'flex',
    padding: '10px 0px 5px 5px',
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
  fileContainer: {
    marginRight: 10,
    border: 'solid 1px #cccccc',
    borderRadius: 4,
    background: 'white'
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
    right: -6,
    bottom: 2,
    color: 'gray',
    height: 20,
    backgroundColor: 'white',
    borderRadius: 10,
    cursor: 'pointer'
  },
  fileAction: {
    right: 1
  },
  remove: {
    height: 20,
    width: 20,
    color: '#3aa3e3',
    '&.pdf-icon': {
      color: '#db4437'
    },
    '&.excel-icon': {
      color: '#238441'
    },
    '&.presentation-icon': {
      color: '#d24625'
    }
  },
  removeAll: {
    color: 'gray',
    display: 'flex',
    marginBottom: -4,
    cursor: 'pointer'
  },
  fileIcon: {
    fontSize: '44px !important',
    color: '#3aa3e3',
    '&.pdf-icon': {
      color: '#db4437'
    },
    '&.excel-icon': {
      color: '#238441'
    },
    '&.presentation-icon': {
      color: '#d24625'
    }
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
        {/* <div className={classes.removeAll}>
          <Tooltip title="Rmove all files" placement="top">
            <DeleteForeverIcon onClick={this.filesRemoveAll} />
          </Tooltip>
        </div> */}
        <div className={classes.files}>
          {files.map((file) => {
            const documentType = getFileType(file.type);
            const icons = FILES_ICONS[documentType];
            const iconClass = (icons && icons.icon) || 'mdi-set mdi-file-outline';
            const isImage = file.preview.type === 'image';
            const closeIconClass = icons && icons.id;
            return (
              <Tooltip title={file.name} placement="top">
                <div className={classNames(classes.file, { [classes.fileContainer]: !isImage })} key={file.id}>
                  {isImage
                    ? <div style={{ backgroundImage: `url("${file.preview.url}")` }} className={classes.image} />
                    : <Icon className={classNames(iconClass, classes.fileIcon)} />}
                  <div className={classNames(classes.action, { [classes.fileAction]: !isImage })}>
                    <Tooltip title={I18n.t('common.remove')} placement="right">
                      <CancelIcon
                        classes={{
                          root: classNames(closeIconClass, classes.remove)
                        }}
                        onClick={() => {
                          this.filesRemoveOne(file);
                        }}
                      />
                    </Tooltip>
                  </div>
                </div>
              </Tooltip>
            );
          })}
        </div>
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(FilesPickerPreview);