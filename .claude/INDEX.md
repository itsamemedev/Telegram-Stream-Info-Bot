# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot_v37.py (300)

```
 10590  GET              /                                                dashboard
 16361  GET              /api/abo/status                                  api_abo_status
 10689  GET              /api/active-recordings                           api_active_recordings
 16436  GET              /api/activity-pulse                              api_activity_pulse
 15686  GET              /api/ai-log                                      api_ai_log
 11087  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 25851  GET              /api/ai/anomalies                                api_ai_anomalies
 12782  POST             /api/ai/ask                                      api_ai_ask
 14020  POST             /api/ai/claude/save                              api_claude_save
 14000  GET              /api/ai/claude/status                            api_claude_status
 14038  POST             /api/ai/claude/test                              api_claude_test
 13048  GET              /api/ai/config                                   api_ai_config
 11259  GET              /api/ai/conversations                            api_ai_conversations_list
 11270  POST             /api/ai/conversations                            api_ai_conversations_create
 11280  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get
 11303  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete
 11310  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch
 11321  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send
 11454  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream
 12123  POST             /api/ai/diagnose                                 api_ai_diagnose
 26089  GET              /api/ai/forecast-storage                         api_ai_forecast_storage
 26123  GET              /api/ai/health-score/<username>                  api_ai_health_score
 11243  GET              /api/ai/models                                   api_ai_models
 25804  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive
 25784  POST             /api/ai/query                                    api_ai_query
 25957  GET              /api/ai/recommendations                          api_ai_recommendations
 26005  GET              /api/ai/report                                   api_ai_report
 26056  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice
 25915  GET              /api/ai/segments                                 api_ai_segments
 25759  GET              /api/ai/skills                                   api_ai_skills
 16196  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 24177  GET/POST         /api/audio/config                                api_audio_config
 24207  POST             /api/audio/testtone                              api_audio_testtone
 16302  GET/POST         /api/auto-archive-rules                          api_archive_rules
 16326  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 16330  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12998  GET              /api/automation/status                           api_automation_status
 13020  POST             /api/automation/toggle                           api_automation_toggle
 14833  GET              /api/azrael/agents                               api_azrael_agents
 12901  POST             /api/azrael/ask                                  api_azrael_ask
 24413  GET/POST         /api/azrael/context                              api_azrael_context
 14460  GET              /api/azrael/core                                 api_azrael_core
 24547  POST             /api/azrael/live_pause                           api_azrael_live_pause
 24537  GET              /api/azrael/live_status                          api_azrael_live_status
 24555  POST             /api/azrael/live_test                            api_azrael_live_test
 14842  GET              /api/azrael/memories                             api_azrael_memories
 24603  POST             /api/azrael/persona                              api_azrael_persona_set
 24594  GET              /api/azrael/personas                             api_azrael_personas
 24631  GET              /api/azrael/piper_status                         api_azrael_piper_status
 24386  POST             /api/azrael/react                                api_azrael_react
 24422  GET              /api/azrael/reaction                             api_azrael_reaction
 24574  GET              /api/azrael/reactions                            api_azrael_reactions
 24624  GET              /api/azrael/transcript                           api_azrael_transcript
 24509  POST             /api/azrael/tts_test                             api_azrael_tts_test
 24484  GET              /api/azrael/voices                               api_azrael_voices
 24648  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11641  GET              /api/backoff-watch                               api_backoff_watch
 15457  POST             /api/backup/run                                  api_backup_run
 15423  GET              /api/backup/status                               api_backup_status
 15412  POST             /api/backup/system                               api_backup_system
 16268  GET              /api/bandwidth/live                              api_bandwidth_live
 16181  GET              /api/bookmarks                                   api_bookmarks_list
 11904  GET              /api/brain                                       api_brain
 11841  GET              /api/brain/alarms                                api_brain_alarms
 11826  GET              /api/brain/creator                               api_brain_creator
 11803  GET              /api/brain/graph                                 api_brain_graph
 11864  GET              /api/brain/growth                                api_brain_growth
 10186  GET              /api/brain/health                                api_brain_health
 25129  GET              /api/channel/categories                          api_channel_categories
 25135  POST             /api/channel/set                                 api_channel_set
 24945  GET              /api/channels/status                             api_channels_status
 23745  POST             /api/chat/send                                   api_chat_send
 15144  GET              /api/chat/send_status                            api_chat_send_status
 10670  GET              /api/checks                                      api_checks
 24450  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 24433  GET              /api/clips                                       api_clips
 24466  POST/DELETE      /api/clips/clear                                 api_clips_clear
 24052  GET              /api/cohost                                      api_cohost
 24064  POST             /api/cohost/config                               api_cohost_config
 16924  GET/POST         /api/collections                                 api_collections
 16959  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify
 17023  GET              /api/collections/<int:cid>/trackings             api_collection_trackings
 17364  GET              /api/community/stats                             api_community_stats
 26461  POST             /api/config/restore                              api_config_restore
 26446  GET              /api/config/snapshot                             api_config_snapshot
 16459  GET              /api/cookies/age                                 api_cookies_age
 10737  GET              /api/cookies/health                              api_cookies_health
 10744  POST             /api/cookies/update                              api_cookies_update
 26412  GET              /api/data/export                                 api_data_export
 17874  GET              /api/db/export                                   api_db_export
 17901  POST             /api/db/import                                   api_db_import
 17861  GET              /api/db/summary                                  api_db_summary
 23978  GET              /api/debug/threads                               api_debug_threads
 27347  GET              /api/defense/attacks                             api_defense_attacks
 27314  GET              /api/defense/crowdsec                            api_defense_crowdsec
 27332  GET              /api/defense/fail2ban                            api_defense_fail2ban
 27038  GET              /api/defense/overview                            api_defense_overview
 15519  POST             /api/discord/announce                            api_discord_announce
 15247  GET              /api/discord/clips_week                          api_discord_clips_week
 15463  GET              /api/discord/community                           api_discord_community
 15172  GET              /api/discord/invite                              api_discord_invite
 14591  GET              /api/discord/overview                            api_discord_overview
 14677  POST             /api/discord/webhook_test                        api_discord_webhook_test
 17441  POST             /api/donations/add                               api_donations_add
 17474  GET              /api/donations/manual                            api_donations_manual
 17482  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 17377  POST             /api/donations/reset                             api_donations_reset
 17498  GET              /api/donations/summary                           api_donations_summary
 16250  GET              /api/events                                      api_events
 15294  GET              /api/events/stream                               api_events_stream
 18529  GET              /api/evolution/changelog                         api_evolution_changelog
 18514  GET              /api/evolution/history                           api_evolution_history
 18454  GET              /api/evolution/learned                           api_evolution_learned
 18476  GET              /api/evolution/proposals                         api_evolution_proposals
 18497  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 18444  POST             /api/evolution/run                               api_evolution_run
 18544  GET              /api/evolution/snapshots                         api_evolution_snapshots
 18409  GET              /api/evolution/status                            api_evolution_status
 17708  GET              /api/finanzamt/entries                           api_finanzamt_entries
 17728  POST             /api/finanzamt/entry                             api_finanzamt_add
 17755  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 16263  GET              /api/forecast/storage                            api_forecast_storage
 13036  GET              /api/freeai/status                               api_freeai_status
 14533  GET              /api/health                                      api_health
 11559  GET              /api/health-score                                api_health_score
 16281  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 16277  GET              /api/heatmap/recordings                          api_heatmap_recordings
 24101  GET              /api/highlights                                  api_highlights
 24113  POST             /api/highlights/config                           api_highlights_config
 16834  GET              /api/insights/activity-clock                     api_insights_activity_clock
 16709  GET              /api/insights/best-times/<username>              api_insights_best_times
 16816  GET              /api/insights/catch-rate                         api_insights_catch_rate
 16791  GET              /api/insights/growth/<username>                  api_insights_growth
 16855  GET              /api/insights/leaderboard                        api_insights_leaderboard
 16742  GET              /api/insights/reliability                        api_insights_reliability
 16765  GET              /api/insights/session-stats                      api_insights_session_stats
 16889  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer
 24986  GET              /api/kick/channel                                api_kick_channel
 25007  POST             /api/kick/channel                                api_kick_channel_set
 14260  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 14328  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 14306  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 14245  GET              /api/kick/oauth/start                            api_kick_oauth_start
 14285  GET              /api/kick/oauth/status                           api_kick_oauth_status
 24225  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 24294  POST             /api/kickmod/config                              api_kickmod_config
 24339  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 24353  GET              /api/kickmod/learned                             api_kickmod_learned
 24380  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 24360  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 24691  POST             /api/kickmod/say                                 api_kickmod_say
 24667  POST             /api/kickmod/start                               api_kickmod_start
 24265  GET              /api/kickmod/status                              api_kickmod_status
 24678  POST             /api/kickmod/stop                                api_kickmod_stop
 10522  POST             /api/login                                       dashboard_login_submit
 17349  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 13487  POST             /api/marketing/config                            api_marketing_config
 13512  GET              /api/marketing/preview                           api_marketing_preview
 13522  POST             /api/marketing/send-now                          api_marketing_send_now
 13461  GET              /api/marketing/status                            api_marketing_status
 13479  POST             /api/marketing/toggle                            api_marketing_toggle
 24128  GET              /api/moderation/feed                             api_moderation_feed
 14091  POST             /api/news/config                                 api_news_config
 14057  GET              /api/news/creators                               api_news_creators
 14068  POST             /api/news/creators/generate                      api_news_creators_generate
 14133  POST             /api/news/generate-now                           api_news_generate_now
 14128  GET              /api/news/items                                  api_news_items
 14119  GET              /api/news/preview                                api_news_preview
 13987  GET              /api/news/status                                 api_news_status
 14083  POST             /api/news/toggle                                 api_news_toggle
 17206  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 15065  GET              /api/notify/status                               api_notify_status
 15076  POST             /api/notify/test                                 api_notify_test
 15051  GET              /api/ops/audit                                   api_ops_audit
 17277  GET              /api/ops/db-stats                                api_ops_db_stats
 17305  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 14857  GET              /api/ops/errors                                  api_ops_errors
 17226  GET              /api/ops/healthcheck                             api_ops_healthcheck
 17956  GET              /api/ops/log-tail                                api_ops_log_tail
 12881  GET              /api/ops/logtail                                 api_ops_logtail
 14798  GET              /api/ops/metrics                                 api_ops_metrics
 14781  GET              /api/ops/resource_history                        api_ops_resource_history
 17930  GET              /api/ops/version                                 api_ops_version
 10940  GET              /api/outcomes                                    api_outcomes
 25610  POST             /api/overlay/config                              api_overlay_config
 25597  POST             /api/overlay/event                               api_overlay_event
 25502  GET              /api/overlay/state                               api_overlay_state
 10973  GET              /api/profile/<username>                          api_profile
 16467  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 16289  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 16415  GET              /api/proxy/heatmap                               api_proxy_heatmap
 16392  GET              /api/proxy/trend                                 api_proxy_trend
 13961  GET              /api/public/stats                                api_public_stats
 10624  GET              /api/pulse                                       api_pulse
 15710  GET              /api/recording-attempts                          api_recording_attempts
 23680  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 23658  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 23699  POST             /api/restream/<int:rid>/start                    api_restream_start
 23999  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 25464  GET              /api/restream/chatfeed                           api_restream_chatfeed
 23634  POST             /api/restream/create                             api_restream_create
 14336  GET              /api/restream/deck                               api_restream_deck
 12972  GET              /api/restream/health                             api_restream_health
 25486  POST             /api/restream/layout                             api_restream_layout
 23607  GET              /api/restream/list                               api_restream_list
 12945  POST             /api/restream/report                             api_restream_report
 24012  POST             /api/restream/start_all                          api_restream_start_all
 24038  POST             /api/restream/stop_all                           api_restream_stop_all
 13235  GET              /api/restream/testpush                           api_testpush_status
 13260  POST             /api/restream/testpush                           api_testpush_run
 17614  GET              /api/restream/verify                             api_restream_verify
 15225  GET              /api/retention/preview                           api_retention_preview
 15234  POST             /api/retention/run                               api_retention_run
 26527  POST             /api/schedule/add                                api_schedule_add
 26517  GET              /api/schedule/list                               api_schedule_list
 26552  POST             /api/schedule/remove                             api_schedule_remove
 15107  POST             /api/scheduler/add                               api_scheduler_add
 15128  POST             /api/scheduler/delete                            api_scheduler_delete
 15094  GET              /api/scheduler/list                              api_scheduler_list
 15182  POST             /api/scheduler/toggle                            api_scheduler_toggle
 16166  GET              /api/search                                      api_search
 27085  GET              /api/selftest                                    api_selftest
 23716  GET              /api/shield/stats                                api_shield_stats
 10643  GET              /api/stats                                       api_stats
 16430  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 16357  GET              /api/stats/tiktok-status                         api_tiktok_status
 26492  GET              /api/stats/timeline                              api_stats_timeline
 10711  GET              /api/storage                                     api_storage
 10718  POST             /api/storage/cleanup                             api_storage_cleanup
 16343  GET              /api/stream/inspect/<username>                   api_stream_inspect
 12922  GET              /api/stream/timeline                             api_stream_timeline
 14665  GET              /api/stream/transcript                           api_stream_transcript
 26160  GET              /api/streamer/compare                            api_streamer_compare
 26359  POST             /api/streamer/delete/<username>                  api_streamer_delete
 15199  GET              /api/streamer/detail                             api_streamer_detail
 26384  GET              /api/streamer/digest/<username>                  api_streamer_digest
 26264  GET              /api/streamer/dormant                            api_streamer_dormant
 26340  GET              /api/streamer/exists/<username>                  api_streamer_exists
 26219  GET              /api/streamer/journal/<username>                 api_streamer_journal
 26184  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 26244  GET              /api/streamer/watchlist                          api_streamer_watchlist
 14500  GET              /api/streamers/wall                              api_streamers_wall
 10860  GET              /api/summary/preview                             api_summary_preview
 15878  GET              /api/system                                      api_system
 15774  GET              /api/system-resources                            api_system_resources
 17562  GET              /api/system/check_timing                         api_check_timing
 17842  GET              /api/system/config_drift                         api_config_drift
 14701  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14912  GET              /api/system/preflight                            api_system_preflight
 15038  GET              /api/system/preflight_history                    api_system_preflight_history
 15359  GET              /api/system/resilience                           api_system_resilience
 16201  GET              /api/tags                                        api_tags_list
 10684  GET              /api/top                                         api_top
 12855  GET              /api/trackings                                   api_trackings
 16994  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 17045  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 16237  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 16450  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 17074  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 16223  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 15549  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 15596  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 15625  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 15607  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 10877  POST             /api/trackings/bulk                              api_trackings_bulk
 15564  GET              /api/trackings/export                            api_trackings_export
 16205  GET              /api/trackings/tags-map                          api_trackings_tags_map
 16505  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11696  GET              /api/trend-7d                                    api_trend_7d
 24498  GET              /api/tts/<fn>                                    api_tts_file
 13115  POST             /api/tunnel/set                                  api_tunnel_set
 13094  GET              /api/tunnel/status                               api_tunnel_status
 13126  POST             /api/tunnel/test                                 api_tunnel_test
 13107  POST             /api/tunnel/toggle                               api_tunnel_toggle
 17814  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 17791  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 17773  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 25638  GET              /api/upload_window                               api_upload_window
 10954  GET              /api/userstats                                   api_userstats
 14144  GET              /api/version                                     api_version
 17113  GET/POST         /api/webhooks                                    api_webhooks
 17153  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete
 17184  POST             /api/webhooks/<int:wid>/test                     api_webhook_test
 17168  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle
 17670  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 17691  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 17655  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 17639  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 30765  GET              /api/youtube/sendrate                            api_youtube_sendrate
 15748  GET              /archive/<int:eid>/download                      archive_download
 15908  GET              /download/<int:recording_id>                     download
 15671  GET              /health                                          health
 23947  GET              /healthz                                         healthz
 10511  GET              /login                                           dashboard_login_page
 10545  GET              /logout                                          dashboard_logout
 10552  GET              /manifest.webmanifest                            pwa_manifest
 14729  GET              /metrics                                         api_prometheus_metrics
 25447  GET              /overlay                                         overlay_page
 10576  GET              /pwa-icon-<variant>.png                          pwa_icon
 10562  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (45)

```
   356  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   620  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   502  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   485  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   477  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   313  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   329  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   664  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   629  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   649  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   536  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
   814  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   896  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   924  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   935  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   801  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   863  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   850  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   831  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   476  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   471  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   519  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   402  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   729  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   493  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   456  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   429  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   703  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   573  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   662  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   568  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   501  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   281  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   746  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   369  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   624  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   779  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   764  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   325  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   563  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   549  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   532  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   589  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   682  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   578  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
```

## Discord-Slash-Commands (45)

```
 27790  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 28249  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 27881  /assign_role            Rolle/Gruppe einem Mitglied geben
 27927  /ban                    Mitglied bannen
 28581  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 28505  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 28545  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 28530  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 28372  /clips                  Letzte Highlight-Clips eines Users
 27842  /create_category        Kategorie anlegen
 27811  /create_channel         Text-Channel anlegen (optional in Kategorie)
 27870  /create_group           Nutzergruppe (= Rolle) anlegen
 27853  /create_role            Rolle / Nutzergruppe anlegen
 27827  /create_voice           Voice-Channel anlegen
 28163  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 28279  /event                  Community-Event ankündigen (Admin) — mit Countdown
 28322  /events                 Kommende Community-Events anzeigen
 28418  /follow                 Bei Live-Gang eines Streamers gepingt werden
 28402  /help                   Alle Bot-Befehle anzeigen
 27916  /kick                   Mitglied kicken
 28145  /leaderboard            Top-10 der Community nach XP
 28358  /livenow                Welche getrackten User sind gerade live
 28388  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 28219  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 27951  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 28131  /rank                   Dein Level und Rang anzeigen
 28345  /recstatus              Aktuell laufende Aufnahmen
 27892  /remove_role            Rolle/Gruppe entfernen
 27804  /restream_status        Restream-Status
 27903  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 28096  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 28114  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 28444  /stats                  Statistik zu einem getrackten Streamer
 27716  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 28740  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 28637  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 28613  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 27938  /timeout                Mitglied stummschalten (Minuten)
 28516  /topstreamers           Rangliste der Streamer nach Aufnahmen
 27746  /track                  TikTok-User tracken
 27730  /tracklist              Getrackte TikTok-User dieses Servers
 28433  /unfollow               Live-Pings für einen Streamer abbestellen
 27779  /untrack                TikTok-User nicht mehr tracken
 28466  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 28490  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 29224  on_member_join
 29186  on_message
 28827  on_raw_reaction_add
 29259  on_ready
```

## Top-Level-Symbole in bot_v37.py (562 Funktionen, 2 Klassen)

```
  2364-2365   _abo_key
  2385-2403   _abo_probe_dump
 26627-26637  _active_recorder_sync
 20920-20927  _ad_allowlist
 22033-22039  _agent_for
 26639-26657  _ai_calls_total_sync
 12768-12778  _ai_dashboard_rate_check
 22042-22058  _ai_telemetry
 22540-22558  _alert
 29372-29422  _alert_monitor_loop
 29796-29858  _announce_loop
  3306-3315   _anthropic_key
  3335-3347   _anthropic_model
  3318-3329   _anthropic_model_raw
 10314-10317  _arg_int
  2356-2361   _as_dict
 19126-19131  _audio_cfg
 22694-22716  _audio_tap_cmd
 10447-10458  _auth_cookie
 10414-10443  _auth_guard
  1512-1517   _auto_on
 23583-23601  _auto_restream_loop
 30926-30941  _azrael_broadcast_reply
 30826-30848  _azrael_chat_reply
 30809-30823  _azrael_chat_should_reply
 13687-13705  _azrael_creator_take
 30854-30856  _azrael_gate_cfg
 22063-22077  _azrael_live_state
 25346-25360  _azrael_overlay_state
 22423-22477  _azrael_proactive_loop
 21882-21938  _azrael_reaction_to_chats
 30859-30866  _azrael_reply_all_chats
 30796-30806  _azrael_self_names
 30894-30923  _azrael_send_to
 22080-22101  _azrael_system
 29536-29539  _backup_active
 29617-29630  _backup_loop
 20808-20809  _badwords_path
 29337-29346  _brain_growth_loop
 11772-11799  _brain_growth_snapshot
  2292-2312   _brain_hint_delay
 11764-11766  _brain_history_for
  6885-6913   _brain_notify
 11741-11762  _brain_record
 11768-11770  _brain_stream_recent
 15273-15290  _browser_push
 11214-11234  _build_context_for_llm
  6929-7016   _build_daily_summary
  2795-2975   _build_native_cmd
 19474-19661  _build_restream_cmd
  3019-3052   _build_ytdlp_cmd
 26579-26586  _cached_probe
  5707-5734   _can_stop_tracking
  1692-1714   _capture_set_cookies
 16553-16565  _cfg_get
 16568-16575  _cfg_set
 25090-25125  _channel_set_all
 18724-18727  _chat_connected
 18730-18746  _chat_disconnected
  8911-8922   _chat_is_forum
 18766-18768  _chat_sanitize
 18770-18779  _chat_src_ok
 18709-18721  _chat_stat
 18749-18752  _chat_stats_snapshot
  3689-3700   _check_ai_alive_sync
  3703-3715   _check_ai_models_sync
 26588-26601  _check_redis_alive_sync
 26603-26623  _check_redis_version_sync
 12463-12506  _classify_pool_anonymity
 12509-12526  _classify_pool_anonymity_bg
   746-750    _claude_chat_sync_metered
 10339-10346  _client_ip
 29890-29917  _clip_prune
 29920-29930  _clip_recfile_for
 30446-30452  _clip_should_velocity
 29971-30053  _clip_to_discord
  3508-3517   _close_ai_session
 30970-30985  _cohost_broadcast
 30952-30956  _cohost_cfg
 31011-31023  _cohost_fire_highlight
 30959-30967  _cohost_gate
 30988-31008  _cohost_highlight
 30102-30136  _community_events_loop
 11157-11193  _conv_add_message
 11196-11201  _conv_archive
 11132-11141  _conv_create
 11146-11154  _conv_messages
 11204-11211  _conv_rename
  7309-7349   _cookie_alarm_loop
  1764-1768   _cookie_autorefresh_info
  1669-1673   _cookie_header
 15323-15355  _cpu_load_snapshot
  3897-3909   _create_index_safe
 13655-13670  _creator_activity
 13711-13734  _creator_dossier_generate
 13673-13684  _creator_facts_line
 26840-26946  _crowdsec_status
 26806-26837  _crowdsec_via_lapi
 26671-26689  _cscli_bin
 26695-26708  _cscli_path
  7202-7227   _daily_summary_loop
 26726-26743  _darf_journal_lesen
 29349-29369  _db_maintenance_loop
  7174-7199   _db_vacuum_loop
 20943-20967  _detect_foreign_ad
  1269-1280   _diag_path_owner
 22329-22373  _director_finalize
 23140-23147  _director_for
 22278-22326  _director_mark
 30340-30375  _disc_automod_check
 30313-30319  _disc_state_get
 30322-30329  _disc_state_set
 27389-27402  _discord_guild_filesize_bytes
 27588-27597  _discord_invite
 30274-30310  _discord_live_thread
 22480-22492  _discord_notify
 27489-27514  _discord_ops_alert
 30172-30270  _discord_post_user
 27653-29334  _discord_run_once
 27527-27585  _discord_start
 29861-29867  _discord_stop
 27410-27412  _discord_upload_limit_label
 27405-27407  _discord_upload_limit_mb
  7230-7304   _disk_alarm_loop
 32239-32288  _disk_autoclean
 32291-32304  _disk_guard_loop
 32231-32236  _disk_pct
 25403-25406  _donations_unknown_count
 19083-19085  _drawtext_chain
 16005-16007  _dump_all_threads
 12388-12452  _enrich_proxies_with_geo
  1909-1953   _ensure_cookie_file_netscape
 27600-27650  _ensure_discord_invite
 30067-30099  _ensure_error_channel
 12631-12668  _ensure_proxy_ready
  8924-8947   _ensure_topic
   627-629    _env_int
   632-634    _env_int_range
 30139-30169  _error_channel_loop
 22524-22537  _event_webhook
 18017-18023  _evo_build_dir
 18026-18033  _evo_version
 18309-18390  _evolution_cycle
 18042-18062  _evolution_llm_note
 18393-18403  _evolution_loop
 18065-18306  _evolution_write_build
  6327-6361   _extract_file_payload
  2041-2043   _extract_urls_from_streamurl_node
 26711-26718  _f2b_sudo_hint
 22560-22562  _faster_whisper_available
 20832-20844  _fetch_ldnoobw_de
 12277-12295  _fetch_proxy_list
 22974-23002  _fetch_tiktok_room_id
   678-681    _ff_cmd
 16690-16703  _ffmpeg_version_str
 19246-19251  _find_chromium
  3012-3016   _find_external_recorder
  2046-2048   _find_stream_urls
 16618-16643  _fire_webhooks
  8085-8094   _fork_safe
   761-770    _freeai_chat_sync_metered
 26761-26803  _geo_lookup_ips
  3497-3506   _get_ai_session
  7919-7959   _get_live_info
  2582-2589   _get_resolve_semaphore
  8273-8638   _handle_single_tracking
 32083-32085  _hb
 32088-32105  _hb_while
 18784-18786  _highlight_cfg
 18789-18818  _highlight_observe
 19254-19259  _htmlov_screenshot_cmd
 22718-22728  _httpx_proxy
 16651-16663  _in_quiet_hours
 33072-33103  _install_fast_eventloop
 10209-10263  _install_fast_json
 16010-16026  _install_faulthandler
 23826-23835  _intel_ensure_schema
 23906-23937  _intel_index_loop
 23847-23857  _intel_index_one
 23838-23844  _intel_semantic
  5696-5705   _is_authorized
  8203-8209   _is_dead
  2031-2033   _is_hevc
 26746-26752  _is_private_ip
  1415-1422   _is_process_running
  6915-6926   _is_quiet_hours
  1077-1086   _is_upload_window
 10298-10311  _json_error_handler
  7132-7162   _kick_broadcaster_id
 13161-13180  _kick_channel_live
  7049-7091   _kick_follower_count
 14223-14236  _kick_oauth_exchange
 14239-14241  _kick_oauth_page
 14182-14186  _kick_redirect_public
 14173-14179  _kick_redirect_source
 14159-14170  _kick_redirect_uri
  7034-7036   _kick_slug
 14189-14220  _kick_user_token
  3946-3954   _kind_from_filename
 16680-16685  _latest_popularity
 20854-20860  _learned_load
 20851-20852  _learned_path
 20862-20870  _learned_save
 23355-23385  _live_react_loop
 23151-23344  _live_react_worker
 21941-21952  _live_transcript_push
 23346-23353  _live_users
 22376-22420  _living_title_loop
  3560-3570   _llm_list_models
 20811-20819  _load_banned_words_file
  1590-1663   _load_cookies_dict
 29542-29614  _local_backup_scan
 10280-10294  _log_5xx
 19669-19673  _looks_like_codec_err
 19664-19666  _looks_like_source_expired
  8166-8196   _loop_fehler
 16030-16039  _loop_heartbeat
 32053-32080  _loop_lag_monitor
 16149-16152  _loop_not_ready
 16042-16110  _loop_watchdog_thread
 21821-21835  _loyalty_add
 21812-21818  _loyalty_get
 21838-21846  _loyalty_top
 17414-17432  _manual_donations_rows
 17435-17437  _manual_donations_total
  8211-8212   _mark_dead
 13328-13357  _marketing_cfg
 13319-13325  _marketing_default_targets
 13314-13316  _marketing_enabled
 13371-13386  _marketing_flavor
 13441-13457  _marketing_loop
 13389-13399  _marketing_post_discord
 13402-13414  _marketing_post_telegram
 13417-13438  _marketing_publish
 13360-13364  _marketing_state_obj
 13367-13368  _marketing_state_save
 30873-30891  _maybe_handle_command
 32390-32414  _maybe_hype_clip
  3864-3887   _migrate_columns
 31148-31159  _mod_is_exempt
 31162-31167  _mod_warn_first
 31170-31173  _mod_warn_text
 18572-18580  _modlog
   881-883    _multistream_targets
  8097-8098   _nc_create_subprocess_exec
  8101-8102   _nc_create_subprocess_shell
 13552-13568  _news_cfg
 13539-13541  _news_enabled
 13606-13647  _news_facts
 13761-13783  _news_generate
 13966-13983  _news_loop
 13544-13549  _news_output_path
 13650-13652  _news_phrase
 13737-13758  _news_phrase_impl
 13581-13588  _news_read
 13571-13574  _news_state_obj
 13577-13578  _news_state_save
 13591-13603  _news_write
 25731-25755  _nl_to_sql
 18610-18612  _normalize_ingest
  2223-2240   _note_check_duration
 21967-21975  _oracle_memories
 22233-22267  _oracle_memorize
 21978-21991  _oracle_persona
 21960-21964  _oracle_recent_text
 18909-18917  _ov_atomic_write
 18897-18903  _ov_bar
 20767-20779  _ov_clip_text
 18906-18907  _ov_oneline
 25414-25443  _overlay_push
 19200-19243  _overlay_render_size
 18671-18675  _overlay_session_reset
 25362-25365  _overlay_src_ok
 20930-20940  _own_invites
 17395-17411  _parse_eur
 19195-19197  _parse_size
 26954-27034  _parse_ssh_attacks
  7521-7554   _pause_resume_cmd
  1718-1762   _persist_refreshed_cookies
  1556-1588   _pick_checked_pull_proxy
 10366-10371  _pin_auth_value
 10403-10404  _pin_clear_fail
 10383-10386  _pin_locked
 10389-10400  _pin_note_fail
 10374-10380  _pin_ok
 25252-25254  _piper_available
 25217-25239  _piper_list_voices
 25259-25284  _piper_pick_model
 25296-25343  _piper_say
 25210-25214  _piper_voice_roots
 16580-16615  _post_json_threaded
 19174-19192  _probe_video_size
  1443-1460   _proc_is_recorder
 12375-12386  _proxy_geo_cache_put
 12602-12628  _proxy_pool_refresh_loop
  1522-1553   _proxy_report_recording
 15995-15997  _prune_stall_dumps
 13786-13907  _public_stats
 22495-22521  _push_notify
 10505-10507  _pwa_dir
 12346-12361  _quick_validate_proxy
 16646-16648  _quiet_hours_config
 10470-10503  _rate_guard
 21786-21792  _react_warn
  8005-8044   _reap_proc
  2263-2285   _record_check_outcome
   673-675    _redact_stream_urls
 12529-12599  _refresh_proxy_pool
 25242-25248  _resolve_piper_model
  2057-2147   _resolve_via_html
  2405-2559   _resolve_via_webcast_api_v2
  2622-2684   _resolve_via_ytdlp
 30492-30621  _resolve_youtube_ingest
 23424-23431  _restream_active_platforms
 18656-18667  _restream_active_sources
 23005-23104  _restream_chat_guardian
 18821-18893  _restream_chat_push
 18583-18595  _restream_enabled
 19262-19349  _restream_html_overlay_start
 19352-19365  _restream_html_overlay_stop
  1025-1027   _restream_layout_mode
 18621-18644  _restream_overlay_files
 23389-23421  _restream_platform_state
 23545-23580  _restream_resume_after_restart
 19413-19471  _restream_tts_enqueue_wav
 19136-19168  _restream_tts_feeder
 19133-19134  _restream_tts_fifo_path
 19368-19395  _restream_tts_start
 19397-19411  _restream_tts_stop
 23434-23542  _restream_verify_loop
 29507-29519  _retention_loop
 29466-29504  _retention_scan
  2367-2369   _room_is_abo
  6365-6482   _run_ai_call
 16133-16146  _run_async_from_flask
 26755-26758  _run_priv
 33060-33068  _run_selfcheck_and_exit
 29522-29533  _s3_client
 25695-25726  _safe_select
  8214-8260   _safe_send
  4848-4864   _sample_net_throughput
 20821-20829  _save_banned_words_file
  2315-2342   _schedule_next_check
 29425-29463  _scheduler_loop
  3890-3894   _schema_pk
 16154-16159  _scraper_session
 31176-31215  _screen_full
 14549-14586  _sec_headers
  2036-2038   _select_stream_from_data_section
 32873-33057  _selfcheck
  1100-1104   _should_defer_upload
 29933-29968  _shrink_for_discord
 32311-32328  _sign_health_check
 32331-32350  _sign_health_loop
  8114-8125   _spawn
  8128-8158   _spawn_from_flask
 27078-27081  _st_befund
 22730-22971  _start_chat_listener
 16113-16130  _start_loop_watchdog
 13931-13957  _stats_loop
 13910-13913  _stats_output_path
 13916-13928  _stats_write
  8706-8720   _storage_cleanup_loop
 32370-32377  _story_for
  3074-3080   _stream_url_expiry
  3089-3095   _stream_url_is_fresh
  3082-3087   _stream_url_ttl
 20894-20901  _streamer_persona_get
 20876-20882  _streamer_personas_load
 20873-20874  _streamer_personas_path
 20884-20892  _streamer_personas_save
 19088-19092  _studio_chain
 29639-29761  _system_backup
 29764-29792  _system_backup_loop
 12298-12337  _test_proxy
 13202-13211  _testpush_cfg
 13214-13231  _testpush_exec
 13183-13199  _testpush_resolve_live
  8883-8893   _tg_topics_load_into_mem
  8880-8881   _tg_topics_path
  8895-8902   _tg_topics_save
 26288-26336  _tiktok_account_exists
 10349-10357  _token_ok
  8905-8909   _topic_forget
 16666-16677  _tracking_max_duration
  1327-1350   _try_attach_file_handler
 25286-25294  _tts_cleanup
 13087-13090  _tunnel_effective
 24712-24765  _twitch_channel_status
 31218-31360  _twitch_chat_loop
 31034-31135  _twitch_eventsub_loop
 17835-17838  _twitch_oauth_page
  1123-1136   _upload_queue_add
  1147-1149   _upload_queue_count
  1106-1115   _upload_queue_load
  1096-1098   _upload_queue_path
  1138-1145   _upload_queue_remove
  1117-1121   _upload_queue_save
  1151-1189   _upload_window_loop
  7978-7985   _uptime_s
 18598-18607  _url_host
   739-743    _usage_record_claude
  7094-7122   _viewer_sample_loop
  7164-7171   _viewer_stats
 10407-10410  _wants_html
  7988-8002   _warn_empty_env
 32126-32221  _watchdog_loop
 30775-30783  _wchat_thank_ok
 22564-22594  _whisper_get_model
  8075-8082   _whisper_native_section
 21773-21779  _whisper_pool
 22663-22692  _whisper_segments
 22596-22660  _whisper_transcribe
 18919-19081  _write_restream_overlay
 31388-31461  _youtube_api_chat_loop
 24768-24871  _youtube_api_status
 24874-24941  _youtube_channel_status
 31464-31621  _youtube_chat_loop
 30627-30640  _youtube_restream_autoconfig
 30643-30667  _youtube_restream_autoconfig_inner
 30733-30761  _youtube_send
 25046-25087  _youtube_set_channel
 30670-30704  _yt_access_token
 30707-30722  _yt_live_chat_id
 31381-31385  _yt_oauth_configured
 30728-30730  _yt_sendrate_cfg
 31363-31378  _yt_timeout
  2606-2607   _ytdlp_detect_available
  2609-2620   _ytdlp_note_result
 16000-16002  _zombie_child_count
  7855-7879   about
  4099-4118   add_ai_log_entry
  3987-3995   add_archive_entry
  4961-4976   add_archive_rule
  4543-4577   add_recording
  4204-4221   add_tracking
  4638-4655   add_tracking_tag
  6485-6518   ai
  3729-3768   ai_chat
  3802-3812   ai_history_append
  3814-3819   ai_history_clear
  3791-3800   ai_history_load
  3776-3789   ai_rate_limit_check
  6547-6555   aireset
 22104-22123  azrael_chat
 31626-31748  brain_cmd
  3098-3282   build_recording_cmd
  4224-4301   bulk_add_trackings
  7352-7411   bulkadd
  8723-8863   check_all_trackings
  4388-4400   claim_live_transition
 20970-21716  class KickModerator
 19676-20654  class RestreamManager
 12713-12755  classify_proxy_anonymity
  6593-6791   cleanup
  5556-5597   cleanup_old_recordings
  4534-4541   clear_recording
 30378-30443  clip_moment
  5109-5152   cluster_failures
  4792-4841   compute_storage_forecast
  7474-7518   cookies_cmd
  5398-5404   cookies_days_old
  4195-4201   count_trackings_for_chat
  4086-4097   decide_preferred_recorder
  4005-4029   delete_archive_entry
  4978-4986   delete_archive_rule
  6022-6169   diag
 31751-31812  einnahmen_cmd
  4786-4789   find_recordings_by_fingerprint
  4047-4063   finish_recording_attempt
  4333-4343   get_all_active_trackings
  4140-4143   get_all_checks
  4579-4582   get_all_recordings
  4680-4690   get_all_tags_with_counts
  4763-4766   get_annotations_for_recording
  3997-4003   get_archive_entry
  4756-4759   get_bookmarked_recordings
  1785-1902   get_cookie_health
  4629-4635   get_event_log
  4070-4084   get_last_recording_attempt
  2687-2792   get_live_status
  5312-5315   get_manual_recordings
  4771-4774   get_or_compute_inspect_sync
  5632-5676   get_outcome_breakdown
  4737-4745   get_priority_poll_interval
  4939-4948   get_profile_snapshots
  4120-4130   get_recent_ai_log
  4065-4068   get_recent_recording_attempts
  4584-4587   get_recording_by_id
  4749-4752   get_recording_note
  3445-3468   get_redis
  4171-4187   get_stats
  5523-5554   get_storage_stats
  4670-4678   get_tags_for_tracking
  5079-5093   get_tiktok_status_distribution
  4724-4735   get_tracking_priority
  4402-4411   get_tracking_state
  4329-4331   get_trackings_for_group
  5328-5331   get_trash_recordings
  9567-10177  handle_recording_finished
  3912-3937   init_db
  5446-5500   inspect_stream_url
 25409-25411  is_revenue_platform
  4951-4959   list_archive_rules
  5826-5864   live
  8263-8271   live_check_worker
  3520-3554   llm_chat
  3619-3686   llm_chat_stream_sync
  3588-3616   llm_chat_sync
  3573-3585   llm_list_models
  4595-4621   log_event
  1377-1410   log_recording_failure
  7668-7717   logs_cmd
 32418-32863  main
  6521-6544   on_ai_media
  7794-7820   on_ai_reply
  7823-7852   on_azrael_mention
  7884-7914   on_callback
 22126-22230  oracle_handle
  7557-7560   pause_tracking
  5686-5691   profile_keyboard
  5407-5443   quick_restart_tracking
  7619-7665   quota
  8640-8703   reaper_loop
  5075-5077   record_tiktok_status
  6560-6590   recstatus
  3470-3478   redis_get_json
  3480-3486   redis_set_json
  4303-4327   remove_tracking
  4657-4668   remove_tracking_tag
 31815-31825  report_cmd
 12758-12760  report_proxy_result
  2150-2177   resolve_tiktok_live_stream
  5323-5326   restore_recording
  7563-7566   resume_tracking
  4989-5069   run_archive_rules
 31828-32033  run_bot
 15922-15969  run_flask
  4867-4912   sample_bandwidth_for_active
  4918-4937   save_profile_snapshot
  4132-4138   save_tiktok_check
  4526-4532   set_recording_file
  4346-4384   set_tracking_paused
  4693-4722   set_tracking_priority
  5318-5321   soft_delete_recording
  8952-9565   split_and_send_video
  5739-5781   start
  4031-4045   start_recording_attempt
  6794-6832   stats
  5293-5310   stop_manual_recording
  7569-7616   stoprec
  7019-7027   summary_cmd
  7720-7791   sysres
  6171-6315   teststream
  5783-5824   tiktok
  7414-7471   topusers
  5901-5958   track
  5866-5898   track_exact
  5972-6020   tracklist
  5159-5291   trigger_manual_recording
  4487-4524   try_acquire_recording_lock
  5334-5393   universal_search
  5960-5970   untrack
  4781-4784   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
archive.py             compute_recording_fingerprint, evaluate_archive_rule, get_archive_entries_paged, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            upsert
channels.py            configure_chat
chatstats.py           summarize
claude.py              build_payload, chat_sync, is_retired, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           class MarketingConfig, class MarketingState, compose, has_content, next_due_ts, should_post, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                build_items, class NewsConfig, class NewsState, item_id, merge, render_json, should_generate
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       looks_like_source_expired, normalize_ingest
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
trackingdb.py          claim_transition, get_state
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
