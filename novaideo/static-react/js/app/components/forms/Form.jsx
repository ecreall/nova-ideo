/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';

import Dialog from '../common/Dialog';
import Scrollbar from '../common/Scrollbar';

const styles = {
  dialogContainer: {
    display: 'block !important',
    position: 'relative',
    height: '100%',
    width: '100%',
    minWidth: 300
  },
  container: {
    padding: '15px 16px',
    '@media (min-width: 600px)': {
      padding: '15px 24px'
    }
  },
  maxContainer: {
    padding: '15px 16px',
    maxWidth: 740,
    marginRight: 'auto',
    marginLeft: 'auto'
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
    fontWeight: 900,
    display: 'flex',
    alignItems: 'center'
  },
  fullAppBarContent: {
    textAlign: 'center'
  },
  footer: {
    display: 'flex',
    justifyContent: 'flex-end',
    padding: '25px 16px',
    '@media (min-width: 600px)': {
      padding: '25px 24px'
    }
  },
  smallPaper: {
    backgroundColor: 'white'
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20
  },
  appBarContainer: {
    flex: 1,
    display: 'flex'
  }
};

export class DumbForm extends React.Component {
  static defaultProps = {
    transition: true
  };

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
    this.setState({ open: false });
  };

  onClose = () => {
    const { onClose } = this.props;
    if (onClose) onClose();
  };

  open = () => {
    this.setState({ open: true });
  };

  render() {
    const { classes, fullScreen, appBar, footer, transition, children, withDrawer, onOpen } = this.props;
    const integretedForm = withDrawer || fullScreen;
    const { open } = this.state;
    const content = (
      <div className={fullScreen ? classes.maxContainer : classes.container}>
        {children}
      </div>
    );
    return (
      <Dialog
        withDrawer={withDrawer}
        transition={transition}
        directDisplay={!fullScreen}
        fullScreen={fullScreen}
        open={open}
        appBar={appBar}
        onClose={this.onClose}
        onOpen={onOpen}
        close={this.close}
        classes={{
          container: classes.dialogContainer,
          closeBtn: classes.closeBtn,
          appBarContent: classNames(classes.appBarContent, {
            [classes.fullAppBarContent]: integretedForm
          }),
          paper: classNames({
            [classes.smallPaper]: !integretedForm
          })
        }}
      >
        <div
          className={classNames(classes.root, {
            [classes.fullRoot]: integretedForm && !footer,
            [classes.fullRootWithFooter]: integretedForm && footer,
            [classes.smallRoot]: !integretedForm
          })}
        >
          {fullScreen
            ? <Scrollbar>
              {content}
            </Scrollbar>
            : content}
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