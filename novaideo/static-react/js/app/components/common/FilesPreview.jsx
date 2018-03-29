/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import Icon from 'material-ui/Icon';
import Zoom from 'material-ui/transitions/Zoom';
import { I18n } from 'react-redux-i18n';
import filesize from 'filesize';

import { FILES_ICONS } from '../../constants';
import { getFileType } from '../../utils/globalFunctions';

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'start',
    flexWrap: 'wrap',
    marginTop: 5,
    marginBottom: 5
  },
  fileContainer: {
    display: 'flex',
    maxWidth: 600,
    minWidth: 240,
    background: '#fff',
    border: '1px solid rgba(0, 0, 0, 0.15)',
    borderRadius: 4,
    padding: 15,
    textDecoration: 'none',
    boxShadow: '0 1px 1px rgba(0, 0, 0, 0.06)',
    position: 'relative',
    marginRight: 5,
    marginBottom: 5
  },
  file: {
    display: 'flex',
    flexDirection: 'column',
    paddingLeft: 3,
    paddingRight: 5,
    marginTop: 2
  },
  fileIcon: {
    fontSize: '32px !important',
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
  fileDown: {
    position: 'absolute',
    left: 31,
    top: 33,
    color: '#3aa3e3',
    padding: 1,
    backgroundColor: '#fff',
    transform: 'scale(0)',
    borderRadius: 8,
    height: 15,
    lineHeight: 'normal !important',
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
  fileTitle: {
    fontSize: 14,
    display: 'block',
    marginBottom: -1,
    fontWeight: 700,
    color: '#2c2d30'
  },
  fileAddon: {
    fontSize: 13,
    color: '#717274',
    lineHeight: 'normal'
  },
  fileAddonZoom: {
    transform: 'scale(0)',
    display: 'inline-block'
  }
};

class FilePrevie extends React.Component {
  state = {
    hover: false
  };

  enter = () => {
    this.setState({ hover: true });
  };

  leave = () => {
    this.setState({ hover: false });
  };

  getDocumentType = () => {
    const { file } = this.props;
    return getFileType(file.mimetype);
  };

  render() {
    const { file, classes } = this.props;
    const { hover } = this.state;
    const documentType = this.getDocumentType();
    const icons = FILES_ICONS[documentType];
    const iconClass = (icons && icons.icon) || 'mdi-set mdi-file-outline';
    const downIconClass = classNames(icons && icons.id, 'mdi-set mdi-arrow-down-bold-circle');
    return (
      <a target="_blank" href={file.url} className={classes.fileContainer} onMouseEnter={this.enter} onMouseLeave={this.leave}>
        <Icon className={classNames(iconClass, classes.fileIcon)} />
        <Zoom in={hover} timeout={100}>
          <Icon className={classNames(downIconClass, classes.fileDown)} />
        </Zoom>
        <div className={classes.file}>
          <div className={classes.fileTitle}>
            {file.title}
          </div>
          <div className={classes.fileAddon}>
            {filesize(file.size)}
            -
            {!hover &&
              documentType &&
              <span>
                {documentType}
              </span>}
            <Zoom in={hover}>
              <span className={classes.fileAddonZoom}>
                {hover && I18n.t('common.clickDownload')}
              </span>
            </Zoom>
          </div>
        </div>
      </a>
    );
  }
}

const FilesPreview = (props) => {
  const { files, classes } = props;
  if (files.length === 0) return null;
  return (
    <div className={classes.container}>
      {files.map((file) => {
        return <FilePrevie file={file} classes={classes} />;
      })}
    </div>
  );
};

export default withStyles(styles)(FilesPreview);