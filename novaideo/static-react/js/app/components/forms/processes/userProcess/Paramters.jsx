/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';
import Zoom from '@material-ui/core/Zoom';
import { withApollo } from 'react-apollo';
import AccountCircleIcon from '@material-ui/icons/AccountCircle';
import VpnKeyIcon from '@material-ui/icons/VpnKey';
import SettingsInputComponentIcon from '@material-ui/icons/SettingsInputComponent';
import WorkIcon from '@material-ui/icons/Work';

import VerticalTab from '../../../common/VerticalTab';
import Form from '../../Form';
import EditProfile from './EditProfile';
import EditPassword from './EditPassword';
import AssignRoles from './AssignRoles';
import UserAvatar from '../../../user/UserAvatar';
import EditApiToken from './EditApiToken';

const styles = {
  maxContainer: {
    padding: 5,
    paddingTop: 35,
    maxWidth: 640
  },
  paper: {
    backgroundColor: 'white !important'
  },
  avatar: {
    width: 36,
    height: 36,
    borderRadius: 4
  },
  header: {
    display: 'flex',
    flexDirection: 'column',
    margin: '0 10px',
    position: 'relative'
  },
  headerTitle: {
    fontSize: 15,
    color: '#2c2d30',
    fontWeight: 900,
    display: 'flex',
    lineHeight: 'normal'
  },
  headerAddOn: {
    color: '#999999ff',
    fontSize: 12,
    lineHeight: 'normal'
  },
  titleContainer: {
    display: 'flex'
  },
  tabPanelRoot: {
    backgroundColor: 'white',
    boxShadow: 'none'
  },
  formTitle: {
    flexGrow: 1
  }
};

export class DumbParamters extends React.Component {
  form = null;

  closeForm = () => {
    this.form.close();
  };

  render() {
    const { account, onClose, classes, theme } = this.props;
    const authorPicture = account && account.picture;
    const authorTitle = account && account.title;
    const func = account && account.function;
    return (
      <Form
        initRef={(form) => {
          this.form = form;
        }}
        open
        fullScreen
        transition={Zoom}
        onClose={onClose}
        classes={{
          closeBtn: classes.closeBtn,
          maxContainer: classes.maxContainer,
          paper: classes.paper
        }}
        appBar={[
          <div className={classes.titleContainer}>
            <UserAvatar picture={authorPicture} title={authorTitle} classes={{ avatar: classes.avatar }} />
            <div className={classes.header}>
              <span className={classes.headerTitle}>{authorTitle}</span>
              <span className={classes.headerAddOn}>{func}</span>
            </div>
          </div>,
          <div className={classes.formTitle}>Paramètres de votre compte</div>
        ]}
      >
        <VerticalTab
          classes={{
            panelRoot: classes.tabPanelRoot
          }}
          tabs={[
            {
              title: 'Profil',
              description: 'Mise à jour de vos coordonnées, modifications des photos et images',
              content: <EditProfile form="edit-profile" key="edit-profile" />,
              Icon: AccountCircleIcon
            },
            {
              title: 'Mot de passe',
              description: 'Modification du mot de passe',
              content: <EditPassword form="edit-password" key="edit-password" />,
              Icon: VpnKeyIcon,
              color: '#d72b3f'
            },
            {
              title: 'Jeton API ',
              description:
                'Le jeton API est un mot de passe à usage unique. C\'est un dispositif de sécurité. Vous pouvez obtenir un jeton API dans cet onglet.',
              content: <EditApiToken />,
              Icon: SettingsInputComponentIcon,
              color: '#ff9000'
            },
            {
              title: 'Rôles',
              description:
                'En tant qu\'administrateur, vous pouvez assigner un rôle à chacun des membres. Accéder ici à cette fonctionnalité',
              content: <AssignRoles form="Assign-roles" key="Assign-roles" />,
              Icon: WorkIcon,
              color: theme.palette.success[800]
            }
          ]}
        />
      </Form>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    globalProps: state.globalProps
  };
};

export default withStyles(styles, { withTheme: true })(withApollo(connect(mapStateToProps)(DumbParamters)));