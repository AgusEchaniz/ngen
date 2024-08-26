import NVD3Chart from 'react-nvd3'
import React, { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'

const FeedGraph = ({ dashboardFeed }) => {
  const { t } = useTranslation()
  const [feed, setFeed] = useState([])

  const filtrarEventosNoCero = (datos) => { //opino que se debe mostrar aquellas fuentes que este asociados a uno amas eventos
    return datos.filter((objeto) => objeto.events_count !== 0)
  }

  useEffect(() => {
    setFeed(filtrarEventosNoCero(dashboardFeed))
  }, [dashboardFeed])

  return (
    <div>
      {
        feed.length > 0 ?
          <NVD3Chart id="chart" height={600} type="pieChart" datum={feed}
                     x="feed_name" y="events_count" donut
                     labelType="percent"/> :
          t('ngen.dashboard.no_events_associated_with_feeds')
      }
    </div>
  )
}

export default FeedGraph