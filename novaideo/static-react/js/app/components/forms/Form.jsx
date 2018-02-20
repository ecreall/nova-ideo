/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import { Scrollbars } from 'react-custom-scrollbars';

import Dialog from '../common/Dialog';
import { styles as scrollbarStyles } from '../CollaborationApp';

const styles = {
  container: {
    display: 'block',
    position: 'relative',
    height: '100%',
    minWidth: 560
  },
  fullRoot: {
    height: 'calc(100vh - 66px)'
  },
  fullRootWithFooter: {
    height: `calc(100vh - ${66 + 87}px)`
  },
  root: {
    overflow: 'auto'
  },
  smallRoot: {
    '@media (min-height:600px)': {
      maxHeight: 'calc(100vh - 250px)'
    },
    '@media (max-height:600px)': {
      maxHeight: 'calc(100vh - 215px)'
    },
    '@media (max-height:550px)': {
      maxHeight: 'calc(100vh - 205px)'
    }
  },
  appBarContent: {
    flex: 1,
    fontWeight: 900
  },
  fullAppBarContent: {
    textAlign: 'center'
  },
  footer: {
    display: 'flex',
    justifyContent: 'flex-end',
    padding: '25px 20px'
  },
  smallPaper: {
    backgroundColor: 'white'
  }
};

export class DumbForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: this.props.open
    };
  }

  componentDidMount() {
    if (this.props.initRef) {
      this.props.initRef(this);
    }
  }

  close = () => {
    const { onClose } = this.props;
    this.setState({ open: false }, () => {
      if (onClose) onClose();
    });
  };

  open = () => {
    this.setState({ open: true });
  };

  render() {
    const { classes, fullScreen, appBar, footer, children } = this.props;
    const { open } = this.state;
    return (
      <Dialog
        transition
        directDisplay={!fullScreen}
        fullScreen={fullScreen}
        open={open}
        appBar={appBar}
        onClose={this.close}
        classes={{
          container: classes.container,
          appBarContent: classNames(classes.appBarContent, {
            [classes.fullAppBarContent]: fullScreen
          }),
          paper: !fullScreen && classes.smallPaper
        }}
      >
        <div
          className={classNames(classes.root, {
            [classes.fullRoot]: fullScreen && !footer,
            [classes.fullRootWithFooter]: fullScreen && footer,
            [classes.smallRoot]: !fullScreen
          })}
        >
          {fullScreen
            ? <Scrollbars
              renderTrackVertical={(props) => {
                return <div {...props} style={{ ...props.style, ...scrollbarStyles.trackVertical }} />;
              }}
              renderThumbVertical={(props) => {
                return <div {...props} style={{ ...props.style, ...scrollbarStyles.thumbVertical }} />;
              }}
            >
              {children}
            </Scrollbars>
            : children}
        </div>
        {footer &&
          <div className={classes.footer}>
            {footer}
          </div>}
      </Dialog>
    );
  }
}

export default withStyles(styles)(DumbForm);