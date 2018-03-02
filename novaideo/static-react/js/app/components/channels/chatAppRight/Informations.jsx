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
  }
};

const InformationsContent = ({ id, onActionClick, kind }) => {
  switch (kind) {
  case 'Idea':
    return <Idea id={id} onActionClick={onActionClick} />;
  case 'Person':
    return <User id={id} onActionClick={onActionClick} />;
  default:
    return null;
  }
};

export class DumbInformations extends React.Component {
  render() {
    const { id, subject, onActionClick, channel, onOpen, open, classes } = this.props;
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
        {open && <InformationsContent id={subject} kind={channel.subject.__typename} onActionClick={onActionClick} />}
      </DetailsSection>
    );
  }
}

export default withStyles(styles)(DumbInformations);