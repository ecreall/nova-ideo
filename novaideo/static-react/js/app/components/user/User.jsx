/* eslint-disable react/no-array-index-key, no-underscore-dangle */
import React from 'react';
import { graphql } from 'react-apollo';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';
import Zoom from '@material-ui/core/Zoom';
import CircularProgress from '@material-ui/core/CircularProgress';
import StarBorderIcon from '@material-ui/icons/StarBorder';
import EmailIcon from '@material-ui/icons/Email';
import Icon from '@material-ui/core/Icon';
import { Translate } from 'react-redux-i18n';
import Grid from '@material-ui/core/Grid';
import classNames from 'classnames';
import VisibilitySensor from 'react-visibility-sensor';
import Button from '@material-ui/core/Button';

import Anchor from '../common/Anchor';
import AllignedActions from '../common/AllignedActions';
import { getActions } from '../../utils/processes';
import PersonData from '../../graphql/queries/PersonData.graphql';
import { ACTIONS } from '../../processes';
import ObjectStats from '../common/ObjectStats';
import CollapsibleText from '../common/CollapsibleText';
import OverlaidTooltip from '../common/OverlaidTooltip';
import Dialog from '../common/Dialog';
import { goTo, get } from '../../utils/routeMap';
import Scrollbar from '../common/Scrollbar';
import UserProcessManager from './UserProcessManager';
import UserAppBar from './UserAppBar';
import UserContentsList from './UserContentsList';
import Footer from '../collaborationApp/Footer';
import { initalsGenerator, getFormattedDate } from '../../utils/globalFunctions';
import UserMenu from './UserMenu';
import IdeasFilter from '../collaborationApp/IdeasFilter';
import Filter from '../common/Filter';

const imgGradient = 'linear-gradient(rgba(0,0,0,0), rgba(0,0,0,0) 34%, rgba(0,0,0,0.2) 66%, rgba(0,0,0,0.2) 83%, rgba(0,0,0,0.6)),';

const styles = (theme) => {
  return {
    root: {
      height: 'calc(100vh - 66px)',
      overflow: 'auto',
      width: '100%'
    },
    container: {
      display: 'block',
      position: 'relative',
      height: '100%'
    },
    maxContainer: {
      maxWidth: 1110,
      marginTop: 25,
      marginRight: 'auto',
      marginLeft: 'auto'
    },
    header: {
      opacity: 1,
      padding: '10px 0'
    },
    headerTitle: {
      fontSize: 20,
      fontWeight: '900',
      marginBottom: 5
    },
    headerAddOn: {
      fontSize: 13,
      color: 'gray'
    },
    body: {
      display: 'flex',
      flexDirection: 'column',
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
    defaultCoverContainer: {
      height: '200px !important'
    },
    imgContainer: {
      backgroundClip: ' padding-box',
      margin: 0,
      height: 300,
      position: 'relative'
    },
    defaultCoverImg: {
      height: '200px !important',
      background: theme.palette.primary[500]
    },
    img: {
      backgroundClip: ' padding-box',
      margin: 0,
      height: 300,
      backgroundPosition: '0 -448px,0 -48px,0 -48px',
      backgroundSize: '100% 300%,100%,100%,100%',
      transition: 'background-position 150ms ease',
      boxShadow: '0px 0px 4px 2px rgba(0, 0, 0, 0.3) inset'
    },
    userImgContainer: {
      backgroundClip: ' padding-box',
      margin: 0,
      height: 150,
      width: 150,
      position: 'absolute',
      top: -140
    },
    userImg: {
      borderRadius: 6,
      backgroundClip: ' padding-box',
      margin: 0,
      height: 150,
      width: 150,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      transition: 'background-position 150ms ease',
      border: 'solid 5px #f3f3f3',
      boxShadow: '0 1px 2px rgba(0, 0, 0, 0.3)'
    },
    userIcon: {
      borderRadius: 6,
      backgroundClip: ' padding-box',
      margin: 0,
      height: 150,
      width: 150,
      backgroundColor: theme.palette.tertiary.color,
      transition: 'background-position 150ms ease',
      border: 'solid 5px #f3f3f3',
      boxShadow: '0 1px 2px rgba(0, 0, 0, 0.3)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      color: 'white',
      fontWeight: 900,
      fontSize: 40
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
    closeBtn: {
      '&::after': {
        display: 'block',
        position: 'absolute',
        top: '50%',
        right: 'auto',
        bottom: 'auto',
        left: -4,
        height: 20,
        transform: 'translateY(-50%)',
        borderRadius: 0,
        borderRight: '1px solid #e5e5e5',
        content: '""',
        color: '#2c2d30'
      }
    },
    userData: {
      padding: 16,
      paddingRight: 25,
      width: 290,
      float: 'right',
      marginTop: 15
    },
    paper: {
      backgroundColor: '#fafafa'
    },
    menuContainer: {
      display: 'flex',
      alignItems: 'center',
      marginBottom: 10
    },
    actionsContainer: {
      height: 45,
      width: 'auto',
      paddingRight: 0,
      paddingLeft: 0
    },
    actionsText: {
      color: '#2c2d30',
      marginRight: 5,
      fontSize: 14,
      fontWeight: 400,
      '&:hover': {
        color: theme.palette.info['700']
      }
    },
    actionsIcon: {
      fontWeight: 100,
      fontSize: '20px !important',
      marginRight: 5,
      marginTop: -2,
      height: 20,
      width: 20
    },
    dataList: {
      margin: '10px 0',
      fontSize: 14,
      color: '#565656'
    },
    dataItem: {
      display: 'flex',
      alignItems: 'center',
      margin: '5px 0'
    },
    dataItemIcon: {
      fontSize: '15px !important',
      marginRight: 5
    },
    goToTop: {
      position: 'fixed',
      bottom: 20,
      right: 20
    },
    goToTopBtn: {
      width: 50,
      height: 50,
      fontSize: 24,
      backgroundColor: theme.palette.tertiary.color,
      color: theme.palette.tertiary.hover.color,
      marginTop: 13,
      '&:hover': {
        backgroundColor: theme.palette.tertiary.color
      }
    },
    goToTopIcon: {
      marginTop: 3,
      marginLeft: 2
    }
  };
};

const UserData = ({ person, classes }) => {
  const { createdAt, email } = person;
  const fCreatedAt = getFormattedDate(createdAt, 'date.format');
  return (
    <div className={classes.dataList}>
      <div className={classes.dataItem}>
        <Icon className={classNames(classes.dataItemIcon, 'mdi-set mdi-calendar-clock')} />
        <span>
          <Translate value="user.subscribed" date={fCreatedAt} />
        </span>
      </div>
      {email && (
        <div className={classes.dataItem}>
          <EmailIcon className={classes.dataItemIcon} />
          <span>{email}</span>
        </div>
      )}
    </div>
  );
};

export class DumbUser extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: true
    };
  }

  appBar = null;

  header = null;

  close = () => {
    this.setState({ open: false }, () => {
      goTo(get('root'));
    });
  };

  onCommentSubmit = () => {
    const { onActionClick } = this.props;
    if (onActionClick) onActionClick();
  };

  updateAppbardUserData(visibility) {
    if (visibility) {
      this.appBar.close();
    } else {
      this.appBar.open();
    }
  }

  scrollToTop = () => {
    const parent = this.header.offsetParent;
    parent.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
  };

  render() {
    const { data, processManager, classes } = this.props;
    const { open } = this.state;
    const person = data.person;
    if (!person) {
      return (
        <div className={classes.progress}>
          <CircularProgress disableShrink size={30} />
        </div>
      );
    }
    const scrollEvent = `${person.id}user-contents`;
    const authorPicture = person.picture;
    const coverPicture = person.coverPicture;
    const isAnonymous = person.isAnonymous;
    const communicationActions = getActions(person.actions, { tags: ACTIONS.communication });
    let imgContent = null;
    if (person.title && !authorPicture) {
      imgContent = <div className={classes.userIcon}>{initalsGenerator(person.title)}</div>;
    }
    return (
      <Dialog
        withDrawer
        withRightApp={false}
        classes={{
          container: classes.container,
          // closeBtn: classes.closeBtn,
          paper: classes.paper
        }}
        appBar={(
          <UserAppBar
            initRef={(appBar) => {
              this.appBar = appBar;
            }}
            person={person}
            processManager={processManager}
          />
        )}
        fullScreen
        open={open}
        onClose={this.close}
        transition={Zoom}
      >
        <div className={classes.root}>
          <Scrollbar scrollEvent={scrollEvent}>
            <Filter
              live
              onOpen={this.scrollToTop}
              id={`${person.id}-filter`}
              Form={IdeasFilter}
              sections={['states', 'examination', 'date']}
            />
            <div
              ref={(header) => {
                this.header = header;
              }}
              className={classNames(classes.imgContainer, { [classes.defaultCoverContainer]: !coverPicture })}
            >
              <div
                className={classNames(classes.img, { [classes.defaultCoverImg]: !coverPicture })}
                style={
                  coverPicture
                    ? {
                      backgroundImage: `${imgGradient} url('${coverPicture.url}')`
                    }
                    : {}
                }
              />
            </div>
            <div className={classes.maxContainer}>
              <div className={classes.container}>
                <div className={classes.body}>
                  <div className={classes.bodyContent}>
                    <Grid container>
                      <Grid item xs={12} md={4}>
                        <div className={classes.userData}>
                          <div className={classes.userImgContainer}>
                            {imgContent || (
                              <div
                                className={classes.userImg}
                                style={{
                                  backgroundImage: `url('${authorPicture && authorPicture.url}')`
                                }}
                              />
                            )}
                          </div>
                          <div className={classes.header}>
                            <VisibilitySensor partialVisibility offset={{ top: 64, bottom: 64 }}>
                              {({ isVisible }) => {
                                this.updateAppbardUserData(isVisible);
                                return <div className={classes.headerTitle}>{person.title}</div>;
                              }}
                            </VisibilitySensor>
                            {!isAnonymous && <div className={classes.headerAddOn}>{person.function}</div>}
                          </div>
                          <div className={classes.menuContainer}>
                            {communicationActions.length > 0 ? (
                              <AllignedActions
                                type="button"
                                actions={communicationActions}
                                onActionClick={processManager.execute}
                                overlayPosition="bottom"
                                classes={{
                                  actionsContainer: classes.actionsContainer,
                                  actionsText: classes.actionsText,
                                  actionsIcon: classes.actionsIcon
                                }}
                              />
                            ) : null}
                            <UserMenu open user={person} onActionClick={processManager.execute} />
                          </div>
                          <CollapsibleText className={classes.text} text={person.description} textLen={150} />
                          <UserData person={person} classes={classes} />
                          <div className={classes.stats}>
                            <OverlaidTooltip
                              tooltip={<Translate value="user.folloers" count={person.nbFollowers} />}
                              placement="top"
                            >
                              <div className={classes.followers}>
                                <StarBorderIcon className={classes.followersIcon} />
                                {person.nbFollowers}
                              </div>
                            </OverlaidTooltip>
                            <ObjectStats id={person.id} />
                          </div>
                        </div>
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <UserContentsList id={person.id} />
                      </Grid>
                      <Grid item xs={12} md={2}>
                        <Footer />
                      </Grid>
                    </Grid>
                  </div>
                </div>
              </div>
            </div>
          </Scrollbar>
          <Anchor
            scrollEvent={scrollEvent}
            getAnchor={() => {
              return this.header;
            }}
            classes={{ container: classes.goToTop }}
          >
            <Button variant="fab" color="primary" className={classes.goToTopBtn}>
              <Icon className={classNames(classes.goToTopIcon, 'mdi-set mdi-chevron-double-up')} />
            </Button>
          </Anchor>
        </div>
      </Dialog>
    );
  }
}

function UserWithProcessManager(props) {
  const { data, onActionClick } = props;
  return (
    <UserProcessManager person={data.person} onActionClick={onActionClick}>
      <DumbUser {...props} />
    </UserProcessManager>
  );
}

export const mapStateToProps = (state) => {
  return {
    previousLocation: state.history.navigation.previous,
    site: state.globalProps.site,
    adapters: state.adapters
  };
};

export default withStyles(styles, { withTheme: true })(
  connect(mapStateToProps)(
    graphql(PersonData, {
      options: (props) => {
        return {
          fetchPolicy: 'cache-and-network',
          variables: {
            id: props.id || (props.params && props.params.userId),
            processIds: [],
            nodeIds: [],
            processTags: [],
            actionTags: [ACTIONS.primary]
          }
        };
      }
    })(UserWithProcessManager)
  )
);