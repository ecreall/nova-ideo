import React from 'react';
import classNames from 'classnames';
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import ErrorIcon from '@material-ui/icons/Error';
import InfoIcon from '@material-ui/icons/Info';
import CloseIcon from '@material-ui/icons/Close';
import IconButton from '@material-ui/core/IconButton';
import SnackbarContentBase from '@material-ui/core/SnackbarContent';
import WarningIcon from '@material-ui/icons/Warning';
import { withStyles } from '@material-ui/core/styles';

const variantIcon = {
  success: CheckCircleIcon,
  warning: WarningIcon,
  error: ErrorIcon,
  info: InfoIcon
};

const styles = (theme) => {
  return {
    success: {
      backgroundColor: theme.palette.success[500]
    },
    error: {
      backgroundColor: theme.palette.danger[500]
    },
    info: {
      backgroundColor: theme.palette.info[500]
    },
    warning: {
      backgroundColor: theme.palette.warning[500]
    },
    icon: {
      fontSize: 20
    },
    iconVariant: {
      opacity: 0.9,
      marginRight: theme.spacing.unit
    },
    message: {
      display: 'flex',
      alignItems: 'center'
    }
  };
};

function SnackbarContent(props) {
  const {
    classes, className, message, onClose, variant, ...other
  } = props;
  const Icon = variantIcon[variant];
  return (
    <SnackbarContentBase
      className={classNames(classes[variant], className)}
      message={(
        <span className={classes.message}>
          <Icon className={classNames(classes.icon, classes.iconVariant)} />
          {message}
        </span>
      )}
      action={(
        <IconButton key="close" aria-label="Close" color="inherit" className={classes.close} onClick={onClose}>
          <CloseIcon className={classes.icon} />
        </IconButton>
      )}
      {...other}
    />
  );
}

export default withStyles(styles)(SnackbarContent);