/* eslint-disable no-underscore-dangle */
import React from 'react';
import { I18n } from 'react-redux-i18n';
import InfoOutlineIcon from 'material-ui-icons/InfoOutline';
import { withStyles } from 'material-ui/styles';

import DetailsSection from './DetailsSection';
import Idea from '../../idea/IdeaPopover';
import User from '../../user/UserPopover';

const styles = {
  listItem: {
    borderTop: 'none'
  },
  ideaContainer: {
    maxWidth: 'inherit'
  }
};

const InformationsContent = ({ id, onActionClick, kind, classes }) => {
  switch (kind) {
  case 'Idea':
    return <Idea id={id} onActionClick={onActionClick} classes={{ container: classes.ideaContainer }} />;
  case 'Person':
    return <User id={id} onActionClick={onActionClick} />;
  default:
    return null;
  }
};

export const DumbInformations = ({ id, subject, onActionClick, channel, onOpen, open, classes }) => {
  return (
    <DetailsSection
      classes={{
        listItem: classes.listItem
      }}
      id={id}
      onOpen={onOpen}
      open={open}
      title={
        <span>
          <span>
            {I18n.t('channels.infoBlockTitle')}
          </span>
        </span>
      }
      Icon={InfoOutlineIcon}
    >
      {open &&
        <InformationsContent id={subject} kind={channel.subject.__typename} onActionClick={onActionClick} classes={classes} />}
    </DetailsSection>
  );
};

export default withStyles(styles)(DumbInformations);