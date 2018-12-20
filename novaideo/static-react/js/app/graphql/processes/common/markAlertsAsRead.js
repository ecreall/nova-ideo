import update from 'immutability-helper';

export default function markAlertsAsRead({ mutate }) {
  return ({ alerts, userId }) => {
    return mutate({
      variables: { userId: userId, alerts: alerts },
      optimisticResponse: {
        __typename: 'Mutation',
        markAlertsAsRead: {
          __typename: 'MarkAlertsAsRead',
          status: true
        }
      },
      updateQueries: {
        Alerts: (prev, { mutationResult, queryVariables }) => {
          if (!mutationResult.data.markAlertsAsRead.status || queryVariables.id !== userId) return false;
          const newAlerts = prev.person.unreadAlertsIds.filter((alert) => { return !alerts.includes(alert); });
          return update(prev, {
            person: {
              unreadAlertsIds: {
                $set: newAlerts
              }
            }
          });
        }
      }
    });
  };
}