/* eslint-disable no-param-reassign */
/* eslint-disable no-underscore-dangle */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import classNames from 'classnames';
import { I18n } from 'react-redux-i18n';
import ListItem from '@material-ui/core/ListItem';
import Moment from 'moment';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ChatBubbleOutlineIcon from '@material-ui/icons/ChatBubbleOutline';
import Icon from '@material-ui/core/Icon';

import { getExaminationValue } from '../idea';
import { goToEntity } from '../../utils/routeMap';

const styles = (theme) => {
  return {
    listItem: {
      paddingLeft: 10,
      paddingRight: 10,
      '&:hover': {
        textDecoration: 'none',
        backgroundColor: 'rgba(0, 0, 0, 0.08)'
      }
    },
    active: {
      cursor: 'pointer'
    },
    unread: {
      backgroundColor: theme.palette.warning[50]
    },
    listItemText: {
      fontSize: 13,
      padding: '0 5px',
      color: 'rgba(0, 0, 0, 0.87)'
    },
    date: {
      marginBottom: 8,
      fontWeight: 600
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
    },
    icon: {
      fontSize: '23px !important'
    },
    support: {
      color: '#4eaf4e'
    },
    oppose: {
      color: '#ef6e18'
    },
    withdraw: {}
  };
};

const ALERT_TYPE = {
  comment: 'comment_alert',
  content: 'content_alert',
  workingGroup: 'working_group_alert',
  moderation: 'moderation_alert',
  examination: 'examination_alert',
  support: 'support_alert',
  admin: 'admin_alert'
};

const COMMENT_KIND = {
  comment: 'comment',
  discuss: 'discuss',
  generalDiscuss: 'general_discuss'
};

const COMMENT_MESSAGES = {
  [COMMENT_KIND.comment]: {
    notRespons: 'alerts.commentAlert.comment.notRespons',
    respons: 'alerts.commentAlert.comment.respons'
  },
  [COMMENT_KIND.discuss]: {
    notRespons: 'alerts.commentAlert.discuss.notRespons',
    respons: 'alerts.commentAlert.discuss.respons'
  },
  [COMMENT_KIND.generalDiscuss]: {
    notRespons: 'alerts.commentAlert.generalDiscuss.notRespons',
    respons: 'alerts.commentAlert.generalDiscuss.respons'
  }
};

const SUPPORT_KIND = {
  support: 'support',
  oppose: 'oppose',
  withdraw: 'withdraw'
};

const SUPPORT_MESSAGES = {
  [SUPPORT_KIND.support]: 'alerts.supportAlert.support',
  [SUPPORT_KIND.oppose]: 'alerts.supportAlert.oppose',
  [SUPPORT_KIND.withdraw]: 'alerts.supportAlert.withdraw'
};

const SUPPORT_ICONS = {
  support: 'mdi-set mdi-arrow-up-drop-circle-outline',
  oppose: 'mdi-set mdi-arrow-down-drop-circle-outline',
  withdraw: 'mdi-set mdi-arrow-left-drop-circle-outline'
};

const CONTENT_KIND = {
  modified: 'modified',
  published: 'published',
  publishedAuthor: 'published_author',
  present: 'present',
  userDeactivated: 'user_deactivated'
};

const CONTENT_MESSAGES = {
  [CONTENT_KIND.modified]: 'alerts.contentAlert.modified',
  [CONTENT_KIND.published]: 'alerts.contentAlert.published',
  [CONTENT_KIND.publishedAuthor]: 'alerts.contentAlert.publishedAuthor',
  [CONTENT_KIND.present]: 'alerts.contentAlert.present',
  [CONTENT_KIND.userDeactivated]: 'alerts.contentAlert.userDeactivated'
};

const CONTENT_ICONS = {
  [CONTENT_KIND.modified]: 'mdi-set mdi-square-edit-outline',
  [CONTENT_KIND.published]: 'mdi-set mdi-earth',
  [CONTENT_KIND.publishedAuthor]: 'mdi-set mdi-earth',
  [CONTENT_KIND.present]: 'mdi-set mdi-share',
  [CONTENT_KIND.userDeactivated]: 'mdi-set mdi-account-off'
};

const MODERATION_KIND = {
  moderation: 'moderation',
  newReport: 'new_report',
  objectArchive: 'object_archive',
  objectRestor: 'object_restor',
  objectCensor: 'object_censor',
  moderateContent: 'moderate_content',
  moderateReport: 'moderate_report'
};

const MODERATION_MESSAGES = {
  [MODERATION_KIND.moderation]: 'alerts.moderationAlert.moderation',
  [MODERATION_KIND.newReport]: 'alerts.moderationAlert.newReport',
  [MODERATION_KIND.objectArchive]: 'alerts.moderationAlert.objectArchive',
  [MODERATION_KIND.objectRestor]: 'alerts.moderationAlert.objectRestor',
  [MODERATION_KIND.objectCensor]: 'alerts.moderationAlert.objectCensor',
  [MODERATION_KIND.moderateContent]: 'alerts.moderationAlert.moderateContent',
  [MODERATION_KIND.moderateReport]: 'alerts.moderationAlert.moderateReport'
};

const MODERATION_ICONS = {
  [MODERATION_KIND.moderation]: 'mdi-set mdi-checkbox-multiple-marked',
  [MODERATION_KIND.newReport]: 'mdi-set mdi-checkbox-multiple-marked',
  [MODERATION_KIND.objectArchive]: 'mdi-set mdi-checkbox-multiple-marked',
  [MODERATION_KIND.objectRestor]: 'mdi-set mdi-checkbox-multiple-marked',
  [MODERATION_KIND.objectCensor]: 'mdi-set mdi-checkbox-multiple-marked',
  [MODERATION_KIND.moderateContent]: 'mdi-set mdi-checkbox-multiple-marked',
  [MODERATION_KIND.moderateReport]: 'mdi-set mdi-checkbox-multiple-marked'
};

const CommentAlert = (props) => {
  const {
    node: { kind, subject, createdAt }, data, isUnread, classes
  } = props;
  const alertKind = kind || 'comment';
  const isRespons = data.is_respons !== 'False';
  const medssageData = COMMENT_MESSAGES[alertKind];
  const createdAtF = Moment(createdAt).format(I18n.t('date.format4'));
  const message = isRespons ? medssageData.respons : medssageData.notRespons;
  const goToSubject = subject
    ? () => {
      return goToEntity(subject.__typename, subject.id);
    }
    : null;
  return (
    <ListItem
      classes={{ root: classNames(classes.listItem, { [classes.active]: goToSubject, [classes.unread]: isUnread }) }}
      onClick={goToSubject}
    >
      <ListItemIcon>
        <ChatBubbleOutlineIcon />
      </ListItemIcon>
      <ListItemText disableTypography classes={{ root: classes.listItemText }}>
        <div className={classes.date}>{createdAtF}</div>
        <div
          dangerouslySetInnerHTML={{
            __html: I18n.t(message, { ...data, subjectTtitle: subject ? subject.title : '' })
          }}
        />
      </ListItemText>
    </ListItem>
  );
};

const SupportAlert = (props) => {
  const {
    node: { kind, subject, createdAt }, data, isUnread, classes
  } = props;
  const alertKind = kind || 'support';
  const message = SUPPORT_MESSAGES[alertKind];
  const createdAtF = Moment(createdAt).format(I18n.t('date.format4'));
  const goToSubject = subject
    ? () => {
      return goToEntity(subject.__typename, subject.id);
    }
    : null;
  const icon = SUPPORT_ICONS[alertKind];
  return (
    <ListItem
      classes={{ root: classNames(classes.listItem, { [classes.active]: goToSubject, [classes.unread]: isUnread }) }}
      onClick={goToSubject}
    >
      <ListItemIcon>
        <Icon className={classNames(classes.icon, classes[alertKind], icon)} />
      </ListItemIcon>
      <ListItemText disableTypography classes={{ root: classes.listItemText }}>
        <div className={classes.date}>{createdAtF}</div>
        <div
          dangerouslySetInnerHTML={{
            __html: I18n.t(message, { ...data, subjectTtitle: subject ? subject.title : '' })
          }}
        />
      </ListItemText>
    </ListItem>
  );
};

const ExaminationAlert = (props) => {
  const {
    node: { subject, createdAt }, data, isUnread, classes
  } = props;
  const message = 'alerts.examinationAlert';
  const createdAtF = Moment(createdAt).format(I18n.t('date.format4'));
  const { title, id, __typename } = subject || {};
  const goToSubject = subject
    ? () => {
      return goToEntity(__typename, id);
    }
    : null;
  const examinationState = subject ? getExaminationValue(subject) : null;
  return (
    <ListItem
      classes={{ root: classNames(classes.listItem, { [classes.active]: goToSubject, [classes.unread]: isUnread }) }}
      onClick={goToSubject}
    >
      <ListItemIcon>
        <Icon
          className={classNames(classes.icon, classes.circle, classes[examinationState], 'mdi-set mdi-checkbox-blank-circle')}
        />
      </ListItemIcon>
      <ListItemText disableTypography classes={{ root: classes.listItemText }}>
        <div className={classes.date}>{createdAtF}</div>
        <div
          dangerouslySetInnerHTML={{
            __html: I18n.t(message, { ...data, subjectTtitle: title || '' })
          }}
        />
      </ListItemText>
    </ListItem>
  );
};

const ContentAlert = (props) => {
  const {
    node: { kind, subject, createdAt }, data, isUnread, classes
  } = props;
  const message = CONTENT_MESSAGES[kind];
  const createdAtF = Moment(createdAt).format(I18n.t('date.format4'));
  const { title, id, __typename } = subject || {};
  const goToSubject = subject
    ? () => {
      return goToEntity(__typename, id);
    }
    : null;
  const icon = CONTENT_ICONS[kind];
  return (
    <ListItem
      classes={{ root: classNames(classes.listItem, { [classes.active]: goToSubject, [classes.unread]: isUnread }) }}
      onClick={goToSubject}
    >
      <ListItemIcon>
        <Icon className={classNames(icon, classes.icon)} />
      </ListItemIcon>
      <ListItemText disableTypography classes={{ root: classes.listItemText }}>
        <div className={classes.date}>{createdAtF}</div>
        <div
          dangerouslySetInnerHTML={{
            __html: I18n.t(message, { ...data, subjectTtitle: title || '' })
          }}
        />
      </ListItemText>
    </ListItem>
  );
};

const ModerationAlert = (props) => {
  const {
    node: { kind, subject, createdAt }, data, isUnread, classes
  } = props;
  const message = MODERATION_MESSAGES[kind];
  const createdAtF = Moment(createdAt).format(I18n.t('date.format4'));
  const { title, id, __typename } = subject || {};
  const goToSubject = subject
    ? () => {
      return goToEntity(__typename, id);
    }
    : null;
  const icon = MODERATION_ICONS[kind];
  return (
    <ListItem
      classes={{ root: classNames(classes.listItem, { [classes.active]: goToSubject, [classes.unread]: isUnread }) }}
      onClick={goToSubject}
    >
      <ListItemIcon>
        <Icon className={classNames(icon, classes.icon)} />
      </ListItemIcon>
      <ListItemText disableTypography classes={{ root: classes.listItemText }}>
        <div className={classes.date}>{createdAtF}</div>
        <div
          dangerouslySetInnerHTML={{
            __html: I18n.t(message, { ...data, subjectTtitle: title || '' })
          }}
        />
      </ListItemText>
    </ListItem>
  );
};

const Alert = (props) => {
  const { node: { id, type, data }, itemProps: { newAlerts } } = props;
  const isUnread = newAlerts.includes(id);
  const dataObj = data.reduce((ojects, item) => {
    ojects[item.key] = item.value;
    return ojects;
  }, {});
  switch (type) {
  case ALERT_TYPE.comment:
    return <CommentAlert {...props} data={dataObj} isUnread={isUnread} />;
  case ALERT_TYPE.support:
    return <SupportAlert {...props} data={dataObj} isUnread={isUnread} />;
  case ALERT_TYPE.examination:
    return <ExaminationAlert {...props} data={dataObj} isUnread={isUnread} />;
  case ALERT_TYPE.content:
    return <ContentAlert {...props} data={dataObj} isUnread={isUnread} />;
  case ALERT_TYPE.moderation:
    return <ModerationAlert {...props} data={dataObj} isUnread={isUnread} />;
  default:
    return null;
  }
};

export default withStyles(styles, { withTheme: true })(Alert);