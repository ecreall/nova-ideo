/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import StarBorderIcon from 'material-ui-icons/StarBorder';
import { Translate, I18n } from 'react-redux-i18n';

import OverlaidTooltip from '../common/OverlaidTooltip';
import Illustration from '../common/Illustration';
import LoginButton from '../common/LoginButton';
import { NOT_LOGGED_2 } from '../../constants';

const styles = (theme) => {
  return {
    container: {
      position: 'relative',
      width: 293,
      backgroundColor: 'white',
      border: 'solid 1px #e7e7e7',
      borderRadius: 8,
      '&:hover': {
        backgroundColor: '#f9f9f9'
      }
    },
    header: {
      position: 'absolute',
      opacity: 1,
      pointerEvents: 'none',
      bottom: 0,
      color: 'white',
      width: 'calc(100% - 20px)',
      padding: 10
    },
    headerTitle: {
      fontSize: 20,
      color: 'white',
      fontWeight: '900',
      marginBottom: 5
    },
    body: {
      display: 'flex',
      flexDirection: 'column',
      padding: 15,
      maxWidth: '100%'
    },
    bodyContent: {
      display: 'flex',
      justifyContent: 'space-between',
      flexDirection: 'column',
      width: '100%',
      height: '100%'
    },
    imgContainer: {
      borderTopRightRadius: 6,
      borderBottomRightRadius: 0,
      borderBottomLeftRadius: 0,
      borderTopLeftRadius: 6,
      backgroundClip: ' padding-box',
      margin: 0,
      height: 224,
      position: 'relative',
      backgroundColor: theme.palette.tertiary.color
    },
    illustrationContainer: {
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100%',
      padding: 0
    },
    imgIllustration: {
      width: 180
    },
    illustrationMessage: {
      textAlign: 'center',
      fontSize: 14,
      marginBottom: 16
    }
  };
};

function DumbAnonymousCard({ classes }) {
  return (
    <div className={classes.container}>
      <div className={classes.imgContainer}>
        <Illustration
          img={NOT_LOGGED_2}
          classes={{
            container: classes.illustrationContainer,
            image: classes.imgIllustration
          }}
        />
        <div className={classes.header}>
          <div className={classes.headerTitle}>
            {I18n.t('common.you')}
          </div>
        </div>
      </div>
      <div className={classes.body}>
        <div className={classes.bodyContent}>
          <div className={classes.illustrationMessage}>
            {I18n.t('user.noUserCard')}
          </div>
          <LoginButton />
        </div>
      </div>
    </div>
  );
}

export default withStyles(styles, { withTheme: true })(DumbAnonymousCard);