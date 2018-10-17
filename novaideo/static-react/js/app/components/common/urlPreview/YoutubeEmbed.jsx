import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import PlayIcon from '@material-ui/icons/PlayCircleOutline';
import CloseIcon from '@material-ui/icons/Close';
import IconButton from '@material-ui/core/IconButton';

const styles = {
  container: {
    height: '100%'
  },
  youtubeEmbed: {
    transitionProperty: 'background-color',
    transitionDuration: '2s',
    height: '100%'
  },
  youtubeThumbnail: {
    position: 'relative',
    marginTop: 5,
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center center',
    backgroundSize: 'contain',
    borderRadius: 4,
    backgroundColor: 'black',
    boxShadow: '0 0 0 1px rgba(0, 0, 0, 0.1) inset',
    width: 360,
    height: 270,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden'
  },
  playButtonContainer: {
    minWidth: 150,
    maxWidth: 225,
    width: '100%',
    padding: '5%',
    borderRadius: 10,
    background: 'rgba(0, 0, 0, 0.4)',
    textAlign: 'center'
  },
  playButton: {
    opacity: 0.8,
    width: 60,
    height: 60,
    '&:hover': {
      opacity: 1
    }
  },
  playButtonIcon: {
    pointerEvents: 'none',
    color: 'white',
    width: 60,
    height: 60
  },
  closeEmbedButton: {
    color: '#545454',
    position: 'absolute',
    backgroundColor: 'white',
    boxShadow: '0 0px 7px rgba(0, 0, 0, 0.6)',
    top: 0,
    right: 0,
    margin: 15,
    '&:hover': {
      backgroundColor: 'rgb(187, 187, 187)'
    }
  },
  youtubeEmbedOpen: {
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    zIndex: 2000,
    position: 'fixed',
    backgroundColor: 'rgba(0, 0, 0, 0.4)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center'
  },
  frame: {
    maxWidth: '100%'
  }
};

export class DumbYoutubeEmbed extends React.Component {
  state = {
    open: false
  };

  closeEmbed = () => {
    return this.setState({ open: false });
  };

  openEmbed = () => {
    return this.setState({ open: true });
  };

  render = () => {
    const { id, classes } = this.props;
    const { open } = this.state;
    return (
      <div className={classes.container}>
        <div className={classes.youtubeEmbed}>
          <div
            className={classes.youtubeThumbnail}
            style={{ backgroundImage: `url(https://img.youtube.com/vi/${id}/mqdefault.jpg)` }}
          >
            <div className={classes.playButtonContainer}>
              <IconButton className={classes.playButton} onClick={this.openEmbed}>
                <PlayIcon className={classes.playButtonIcon} />
              </IconButton>
            </div>
          </div>
        </div>
        {open && (
          <div className={classes.youtubeEmbedOpen} onClick={this.closeEmbed}>
            <iframe
              title="YouTube video"
              id="ytplayer"
              type="text/html"
              width="640"
              height="360"
              className={classes.frame}
              src={`https://www.youtube.com/embed/${id}?autoplay=1`}
              frameBorder="0"
            />
            <IconButton className={classes.closeEmbedButton} color="primary" onClick={this.closeEmbed}>
              <CloseIcon />
            </IconButton>
          </div>
        )}
      </div>
    );
  };
}

export default withStyles(styles)(DumbYoutubeEmbed);