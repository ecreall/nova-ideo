/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import { graphql } from 'react-apollo';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import StarBorderIcon from '@material-ui/icons/StarBorder';
import { Translate } from 'react-redux-i18n';
import classNames from 'classnames';
import Icon from '@material-ui/core/Icon';

import { getActions, filterActions } from '../../utils/processes';
import { goTo, get } from '../../utils/routeMap';
import UserProcessManager from './UserProcessManager';
import { closeChatApp } from '../../actions/chatAppActions';
import PersonData from '../../graphql/queries/PersonData.graphql';
import { ACTIONS, PROCESSES } from '../../processes';
import ObjectStats from '../common/ObjectStats';
import CollapsibleText from '../common/CollapsibleText';
import OverlaidTooltip from '../common/OverlaidTooltip';
import AllignedActions from '../common/AllignedActions';
import UserMenu from './UserMenu';
import Comment from '../forms/processes/common/Comment';
import { initalsGenerator, getFormId } from '../../utils/globalFunctions';

const imgGradient =
  'linear-gradient(rgba(0,0,0,0), rgba(0,0,0,0) 34%, rgba(0,0,0,0.2) 66%, rgba(0,0,0,0.2) 83%, rgba(0,0,0,0.6)),';

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
    headerAddOn: {
      color: 'white',
      fontSize: 13
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
    bodyFooter: {
      display: 'flex',
      flexDirection: 'row',
      marginTop: 15
    },
    text: {
      fontSize: 13,
      lineHeight: 1.48,
      marginBottom: 10,
      '& a': {
        color: '#0576b9',
        textDecoration: 'none',
        '&:hover': {
          textDecoration: 'underline'
        }
      },
      '& p': {
        margin: 0
      }
    },
    progress: {
      width: '100%',
      minWidth: 320,
      minHeight: 340,
      display: 'flex',
      justifyContent: 'center'
    },
    formContainer: {
      padding: 10,
      paddingRight: 10,
      paddingLeft: 10,
      backgroundColor: '#ededed',
      boxShadow: '0 -1px 0 rgba(0,0,0,.1)',
      borderRadius: 0
    },
    imgContainer: {
      borderTopRightRadius: 6,
      borderBottomRightRadius: 0,
      borderBottomLeftRadius: 0,
      borderTopLeftRadius: 6,
      backgroundClip: ' padding-box',
      margin: 0,
      height: 224,
      position: 'relative'
    },
    img: {
      cursor: 'pointer',
      borderTopRightRadius: 6,
      borderBottomRightRadius: 0,
      borderBottomLeftRadius: 0,
      borderTopLeftRadius: 6,
      backgroundClip: ' padding-box',
      margin: 0,
      height: 224,
      backgroundPosition: '0 -448px,0 -48px,0 -48px',
      backgroundSize: '100% 300%,100%,100%,100%',
      transition: 'background-position 150ms ease'
    },
    imgAnonymous: {
      cursor: 'initial'
    },
    stats: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'flex-end'
    },
    followers: {
      display: 'flex',
      alignItems: 'flex-end',
      height: 23,
      color: '#2c2d30'
    },
    followersIcon: {
      marginRight: 3
    },
    actions: {
      paddingBottom: 16,
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      borderBottom: 'solid 1px rgba(128, 128, 128, 0.3)',
      marginBottom: 16,
      marginTop: 1
    },
    actionsContainer: {
      width: 'initial'
    },
    userIcon: {
      fontSize: '50px !important',
      float: 'right',
      color: 'white',
      padding: 5
    },
    noImgContainer: {
      backgroundColor: theme.palette.tertiary.color
    }
  };
};

export class DumbUserCard extends React.Component {
  openDetails = () => {
    const { onActionClick } = this.props;
    if (onActionClick) onActionClick();
    this.props.closeChatApp();
    goTo(get('users', { userId: this.props.data.person.id }));
  };

  onCommentSubmit = () => {
    const { onActionClick } = this.props;
    if (onActionClick) onActionClick();
  };

  render() {
    const { data, processManager, withCommentForm, classes } = this.props;
    const person = data.person;
    if (!person) {
      return (
        <div className={classes.progress}>
          <CircularProgress size={30} />
        </div>
      );
    }
    const communicationActions = getActions(person.actions, { tags: ACTIONS.communication });
    const commentAction = filterActions(communicationActions, { behaviorId: PROCESSES.usermanagement.nodes.discuss.nodeId })[0];
    const channel = person.channel;
    const channelId = channel ? channel.id : `${person.id}-channel`;
    const authorPicture = person.picture;
    const isAnonymous = person.isAnonymous;
    let imgContent = null;
    if (isAnonymous) {
      imgContent = <Icon className={classNames(classes.userIcon, 'mdi-set mdi-guy-fawkes-mask')} />;
    } else if (person.title && !authorPicture) {
      imgContent = <div className={classes.userIcon}>{initalsGenerator(person.title)}</div>;
    }
    return [
      <div className={classes.container}>
        <div
          className={classNames(classes.imgContainer, { [classes.noImgContainer]: imgContent })}
          onClick={!isAnonymous ? this.openDetails : null}
        >
          {!imgContent ? (
            <div
              className={classNames(classes.img, { [classes.imgAnonymous]: isAnonymous })}
              style={{
                backgroundImage: `${imgGradient} url('${authorPicture && authorPicture.url}')`
              }}
            />
          ) : (
            imgContent
          )}
          <div className={classes.header}>
            <div className={classes.headerTitle}>{person.title}</div>
            {!isAnonymous && <div className={classes.headerAddOn}>{person.function}</div>}
          </div>
        </div>
        <div className={classes.body}>
          {!isAnonymous
            ? [
              <div className={classes.actions}>
                {communicationActions.length > 0 && (
                  <AllignedActions
                    type="button"
                    actions={communicationActions}
                    onActionClick={processManager.execute}
                    classes={{ actionsContainer: classes.actionsContainer }}
                  />
                )}
                <UserMenu open user={person} onActionClick={processManager.execute} />
              </div>,
              <div className={classes.bodyContent}>
                <CollapsibleText className={classes.text} text={person.description} textLen={150} />
                <div className={classes.stats}>
                  <OverlaidTooltip tooltip={<Translate value="user.folloers" count={person.nbFollowers} />} placement="top">
                    <div className={classes.followers}>
                      <StarBorderIcon className={classes.followersIcon} />
                      {person.nbFollowers}
                    </div>
                  </OverlaidTooltip>
                  <ObjectStats id={person.id} />
                </div>
              </div>
            ]
            : null}
        </div>
      </div>,
      withCommentForm && commentAction ? (
        <Comment
          isDiscuss
          classes={{ container: classes.formContainer }}
          form={getFormId(channelId)}
          action={commentAction}
          context={person.oid}
          subject={person.oid}
          channel={person.channel}
          onSubmit={this.onCommentSubmit}
        />
      ) : null
    ];
  }
}

export const mapDispatchToProps = {
  closeChatApp: closeChatApp
};

function UserCardWithProcessManager(props) {
  const { data, onActionClick } = props;
  return (
    <UserProcessManager person={data.person} onActionClick={onActionClick}>
      <DumbUserCard {...props} />
    </UserProcessManager>
  );
}

export default withStyles(styles)(
  connect(
    null,
    mapDispatchToProps
  )(
    graphql(PersonData, {
      options: (props) => {
        return {
          fetchPolicy: 'cache-and-network',
          variables: {
            id: props.id,
            processIds: [],
            nodeIds: [],
            processTags: [],
            actionTags: [ACTIONS.primary]
          }
        };
      }
    })(UserCardWithProcessManager)
  )
);