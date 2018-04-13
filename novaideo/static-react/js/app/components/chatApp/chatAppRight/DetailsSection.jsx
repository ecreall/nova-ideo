import React from 'react';
import { withStyles } from 'material-ui/styles';

import ContentCollapse from '../../common/ContentCollapse';

export const stylesContentCollapse = (theme) => {
  return {
    entered: {
      height: 'auto !important'
    },
    listItem: {
      background: '#fff',
      borderTop: '1px solid #e8e8e8',
      position: 'relative',
      paddingLeft: 16,
      paddingRight: 8,
      minHeight: 61,
      maxHeight: 61,
      overflowY: 'hidden',
      '&:hover': {
        backgroundColor: '#f9f9f9'
      }
    },
    listItemActive: {
      backgroundColor: '#fff',
      '&:hover': {
        backgroundColor: '#fff'
      }
    },
    titleText: {
      color: '#2c2d30',
      fontSize: 15,
      opacity: 0.9,
      padding: 0,
      whiteSpace: 'nowrap',
      textOverflow: 'ellipsis',
      overflow: 'hidden',
      '&:hover': {
        opacity: 1
      }
    },
    titleTextActive: {
      opacity: 1,
      fontWeight: '700',
      color: '#2c2d30',
      '&:hover': {
        color: '#2c2d30'
      }
    },
    sectionIcon: {
      width: 24,
      height: 24,
      marginRight: 7,
      marginTop: 0,
      fontSize: '18px !important',
      color: theme.palette.info[500]
    },
    sectionIconActive: {
      color: theme.palette.info[500],
      '&:hover': {
        color: theme.palette.info[500]
      }
    },
    icon: {
      color: '#2c2d30',
      opacity: 0.9,
      '&:hover': {
        opacity: 1
      }
    },
    iconActive: {
      opacity: 1,
      color: '#2c2d30',
      '&:hover': {
        color: '#2c2d30'
      }
    }
  };
};

export const DumbDetailsSection = ({ id, title, children, Icon, onOpen, open, classes }) => {
  return (
    <ContentCollapse
      classes={{
        entered: classes.entered,
        listItem: classes.listItem,
        listItemActive: classes.listItemActive,
        text: classes.titleText,
        textActive: classes.titleTextActive,
        sectionIcon: classes.sectionIcon,
        sectionIconActive: classes.sectionIconActive,
        icon: classes.icon,
        iconActive: classes.iconActive
      }}
      id={id}
      onOpen={onOpen}
      open={open}
      title={title}
      Icon={Icon}
    >
      {children}
    </ContentCollapse>
  );
};

export default withStyles(stylesContentCollapse, { withTheme: true })(DumbDetailsSection);