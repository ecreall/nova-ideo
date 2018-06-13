import React from 'react';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';
import { Translate } from 'react-redux-i18n';

import Login from '../forms/processes/userProcess/Login';
import Button from '../styledComponents/Button';
import { filterActions } from '../../utils/processes';
import { ACTIONS, PROCESSES } from '../../processes';

const styles = {
  button: {
    whiteSpace: 'initial !important'
  }
};

export class DumbLoginButton extends React.Component {
  state = {
    open: false
  };

  open = () => {
    this.setState({ open: true });
  };

  close = () => {
    this.setState({ open: false });
  };

  render() {
    const { rootActions, site, color, classes, theme } = this.props;
    const { open } = this.state;
    const userProcessNodes = PROCESSES.usermanagement.nodes;
    const loginAction = filterActions(rootActions, {
      tags: [ACTIONS.mainMenu, ACTIONS.site],
      behaviorId: userProcessNodes.login.nodeId
    })[0];
    return (
      loginAction && [
        <Button onClick={this.open} background={color || theme.palette.success[500]} className={classes.button}>
          <Translate value={loginAction.title} siteTitle={site.title} />
        </Button>,
        open && <Login action={loginAction} onClose={this.close} />
      ]
    );
  }
}

export const mapStateToProps = (state) => {
  return {
    site: state.globalProps.site,
    rootActions: state.globalProps.rootActions
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(DumbLoginButton));