import React from 'react';
import Slider from 'rc-slider';
import Moment from 'moment';
import { I18n, Translate } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';
import classNames from 'classnames';

import AddDeadline from '../forms/processes/adminProcess/AddDeadline';
import EditDeadline from '../forms/processes/adminProcess/EditDeadline';
import Tooltip from '../common/overlay/Tooltip';
import OverlayTrigger from '../common/overlay/OverlayTrigger';
import { getFormattedDate } from '../../utils/globalFunctions';
import { PROCESSES } from '../../processes';
import { getActions } from '../../utils/processes';

const styles = {
  handleContainer: { position: 'absolute', opacity: '1 !important' },
  inner: { opacity: '1 !important', padding: '15px !important' },
  message: { maxWidth: 250, fontWeight: 900 },
  active: { cursor: 'pointer !important' },
  editMessage: {
    marginTop: 10,
    opacity: 0.9
  }
};

class DeadLineBtn extends React.Component {
  state = { open: false };

  getActionData = () => {
    const { date, isExpired, rootActions } = this.props;
    const { addDeadline, editDeadline } = PROCESSES.novaideoabstractprocess.nodes;
    const actions = getActions(rootActions, { behaviorId: [editDeadline.nodeId, addDeadline.nodeId] });
    const editAction = actions.find((a) => {
      return a.nodeId === editDeadline.nodeId;
    });
    const addAction = actions.find((a) => {
      return a.nodeId === addDeadline.nodeId;
    });
    const noDate = isExpired || !date;
    const action = noDate ? addAction : editAction;
    let ActionComponent = null;
    if (action) {
      ActionComponent = noDate ? AddDeadline : EditDeadline;
    }
    return { noDate: noDate, action: action, ActionComponent: ActionComponent };
  };

  toggleCalendar = () => {
    this.setState((prevState) => {
      return { open: !prevState.open };
    });
  };

  render() {
    const {
      date, isExpired, color, classes, value, dragging, index, site, rootActions, className, ...restProps
    } = this.props;
    const { open } = this.state;
    const dateF4 = date ? getFormattedDate(date, 'date.format4') : null;
    const { noDate, action, ActionComponent } = this.getActionData();
    const handle = (
      <Slider.Handle
        className={classNames(className, { [classes.active]: action })}
        onClick={this.toggleCalendar}
        value={value}
        {...restProps}
      />
    );
    return ActionComponent && open ? (
      <React.Fragment>
        {handle}
        <ActionComponent root={site} action={action} date={noDate ? Moment() : date} onClose={this.toggleCalendar} />
      </React.Fragment>
    ) : (
      <OverlayTrigger
        overlay={(
          <Tooltip color={color} className={classes.handleContainer} innerClassName={classes.inner}>
            <div className={classes.message}>
              {date ? (
                <Translate value={isExpired ? 'examination.expiredDeadline' : 'examination.examinationDate'} date={dateF4} />
              ) : (
                I18n.t('examination.noExaminationDate')
              )}
              {action ? <div className={classes.editMessage}>{I18n.t('examination.edit')}</div> : null}
            </div>
          </Tooltip>
        )}
        placement="bottom"
      >
        {handle}
      </OverlayTrigger>
    );
  }
}

export const mapStateToProps = (state) => {
  return {
    site: state.globalProps.site,
    rootActions: state.globalProps.rootActions
  };
};

export default withStyles(styles)(connect(mapStateToProps)(DeadLineBtn));