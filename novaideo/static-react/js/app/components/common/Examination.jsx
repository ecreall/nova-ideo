import React from 'react';
import Icon from '@material-ui/core/Icon';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import { Translate } from 'react-redux-i18n';

import Dialog from './Dialog';
import OverlaidTooltip from './OverlaidTooltip';

const styles = {
  container: {
    padding: '20px 25px',
    width: '100%',
    fontSize: 17,
    lineHeight: 1.5
  },
  titleContainer: {
    fontWeight: 900
  },
  title: {
    marginLeft: 5
  },
  circleContainer: {
    cursor: 'pointer'
  },
  circle: {
    color: 'gray',
    fontSize: 22
  },
  top: {
    color: '#f13b2d',
    textShadow: '0 0px 4px #f13b2d'
  },
  middle: {
    color: '#ef6e18',
    textShadow: '0 0px 4px #ef6e18'
  },
  bottom: {
    color: '#4eaf4e',
    textShadow: '0 0px 4px #4eaf4e'
  }
};

export class DumbExamination extends React.Component {
  state = {
    open: false
  };

  handleClickOpen = () => {
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  render() {
    const { value, title, message, classes } = this.props;
    const icon = <Icon className={classNames(classes.circle, classes[value], 'mdi-set mdi-checkbox-blank-circle')} />;
    return [
      <div className={classes.circleContainer} onClick={this.handleClickOpen}>
        <OverlaidTooltip tooltip={<Translate value="common.examinationClick" name={title} />} placement="top">
          {icon}
        </OverlaidTooltip>
      </div>,
      this.state.open && (
        <Dialog
          directDisplay
          appBar={
            <div className={classes.titleContainer}>
              {icon}
              <span className={classes.title}>{title}</span>
            </div>
          }
          open={this.state.open}
          onClose={this.handleClose}
        >
          <div className={classes.container}>{message}</div>
        </Dialog>
      )
    ];
  }
}

export default withStyles(styles)(DumbExamination);