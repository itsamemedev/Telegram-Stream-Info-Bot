# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (265)

```
 10724  GET              /                                                dashboard
 15828  GET              /api/abo/status                                  api_abo_status
 10832  GET              /api/active-recordings                           api_active_recordings
 15903  GET              /api/activity-pulse                              api_activity_pulse
 15256  GET              /api/ai-log                                      api_ai_log
 11310  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 15663  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 23809  GET/POST         /api/audio/config                                api_audio_config
 23839  POST             /api/audio/testtone                              api_audio_testtone
 15769  GET/POST         /api/auto-archive-rules                          api_archive_rules
 15793  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 15797  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12599  GET              /api/automation/status                           api_automation_status
 12621  POST             /api/automation/toggle                           api_automation_toggle
 14414  GET              /api/azrael/agents                               api_azrael_agents
 12491  POST             /api/azrael/ask                                  api_azrael_ask
 24045  GET/POST         /api/azrael/context                              api_azrael_context
 14041  GET              /api/azrael/core                                 api_azrael_core
 24179  POST             /api/azrael/live_pause                           api_azrael_live_pause
 24169  GET              /api/azrael/live_status                          api_azrael_live_status
 24187  POST             /api/azrael/live_test                            api_azrael_live_test
 14423  GET              /api/azrael/memories                             api_azrael_memories
 24235  POST             /api/azrael/persona                              api_azrael_persona_set
 24226  GET              /api/azrael/personas                             api_azrael_personas
 24263  GET              /api/azrael/piper_status                         api_azrael_piper_status
 24018  POST             /api/azrael/react                                api_azrael_react
 24054  GET              /api/azrael/reaction                             api_azrael_reaction
 24206  GET              /api/azrael/reactions                            api_azrael_reactions
 24256  GET              /api/azrael/transcript                           api_azrael_transcript
 24141  POST             /api/azrael/tts_test                             api_azrael_tts_test
 24116  GET              /api/azrael/voices                               api_azrael_voices
 24280  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11405  GET              /api/backoff-watch                               api_backoff_watch
 15027  POST             /api/backup/run                                  api_backup_run
 14993  GET              /api/backup/status                               api_backup_status
 14982  POST             /api/backup/system                               api_backup_system
 15735  GET              /api/bandwidth/live                              api_bandwidth_live
 15648  GET              /api/bookmarks                                   api_bookmarks_list
 11668  GET              /api/brain                                       api_brain
 11605  GET              /api/brain/alarms                                api_brain_alarms
 11590  GET              /api/brain/creator                               api_brain_creator
 11567  GET              /api/brain/graph                                 api_brain_graph
 11628  GET              /api/brain/growth                                api_brain_growth
 10278  GET              /api/brain/health                                api_brain_health
 24761  GET              /api/channel/categories                          api_channel_categories
 24767  POST             /api/channel/set                                 api_channel_set
 24577  GET              /api/channels/status                             api_channels_status
 23410  POST             /api/chat/send                                   api_chat_send
 14681  GET              /api/chat/send_status                            api_chat_send_status
 10813  GET              /api/checks                                      api_checks
 24082  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 24065  GET              /api/clips                                       api_clips
 24098  POST/DELETE      /api/clips/clear                                 api_clips_clear
 23684  GET              /api/cohost                                      api_cohost
 23696  POST             /api/cohost/config                               api_cohost_config
 16467  GET              /api/community/stats                             api_community_stats
 25761  POST             /api/config/restore                              api_config_restore
 25746  GET              /api/config/snapshot                             api_config_snapshot
 15926  GET              /api/cookies/age                                 api_cookies_age
 10880  GET              /api/cookies/health                              api_cookies_health
 10887  POST             /api/cookies/update                              api_cookies_update
 25712  GET              /api/data/export                                 api_data_export
 17079  GET              /api/db/export                                   api_db_export
 17106  POST             /api/db/import                                   api_db_import
 17066  GET              /api/db/summary                                  api_db_summary
 23610  GET              /api/debug/threads                               api_debug_threads
 26647  GET              /api/defense/attacks                             api_defense_attacks
 26614  GET              /api/defense/crowdsec                            api_defense_crowdsec
 26632  GET              /api/defense/fail2ban                            api_defense_fail2ban
 26338  GET              /api/defense/overview                            api_defense_overview
 15089  POST             /api/discord/announce                            api_discord_announce
 14817  GET              /api/discord/clips_week                          api_discord_clips_week
 15033  GET              /api/discord/community                           api_discord_community
 14709  GET              /api/discord/invite                              api_discord_invite
 14172  GET              /api/discord/overview                            api_discord_overview
 14258  POST             /api/discord/webhook_test                        api_discord_webhook_test
 16544  POST             /api/donations/add                               api_donations_add
 16577  GET              /api/donations/manual                            api_donations_manual
 16585  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 16480  POST             /api/donations/reset                             api_donations_reset
 16601  GET              /api/donations/summary                           api_donations_summary
 15717  GET              /api/events                                      api_events
 14864  GET              /api/events/stream                               api_events_stream
 17832  GET              /api/evolution/changelog                         api_evolution_changelog
 17817  GET              /api/evolution/history                           api_evolution_history
 17757  GET              /api/evolution/learned                           api_evolution_learned
 17779  GET              /api/evolution/proposals                         api_evolution_proposals
 17800  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 17747  POST             /api/evolution/run                               api_evolution_run
 17847  GET              /api/evolution/snapshots                         api_evolution_snapshots
 17712  GET              /api/evolution/status                            api_evolution_status
 16884  GET              /api/finanzamt/entries                           api_finanzamt_entries
 16904  POST             /api/finanzamt/entry                             api_finanzamt_add
 16931  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 15730  GET              /api/forecast/storage                            api_forecast_storage
 12637  GET              /api/freeai/status                               api_freeai_status
 14114  GET              /api/health                                      api_health
 15748  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 15744  GET              /api/heatmap/recordings                          api_heatmap_recordings
 23733  GET              /api/highlights                                  api_highlights
 23745  POST             /api/highlights/config                           api_highlights_config
 24618  GET              /api/kick/channel                                api_kick_channel
 24639  POST             /api/kick/channel                                api_kick_channel_set
 13841  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 13909  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 13887  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 13826  GET              /api/kick/oauth/start                            api_kick_oauth_start
 13866  GET              /api/kick/oauth/status                           api_kick_oauth_status
 23857  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 23926  POST             /api/kickmod/config                              api_kickmod_config
 23971  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 23985  GET              /api/kickmod/learned                             api_kickmod_learned
 24012  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 23992  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 24323  POST             /api/kickmod/say                                 api_kickmod_say
 24299  POST             /api/kickmod/start                               api_kickmod_start
 23897  GET              /api/kickmod/status                              api_kickmod_status
 24310  POST             /api/kickmod/stop                                api_kickmod_stop
 10658  POST             /api/login                                       dashboard_login_submit
 16452  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 13052  POST             /api/marketing/config                            api_marketing_config
 13077  GET              /api/marketing/preview                           api_marketing_preview
 13087  POST             /api/marketing/send-now                          api_marketing_send_now
 13026  GET              /api/marketing/status                            api_marketing_status
 13044  POST             /api/marketing/toggle                            api_marketing_toggle
 23760  GET              /api/moderation/feed                             api_moderation_feed
 13605  POST             /api/news/config                                 api_news_config
 13571  GET              /api/news/creators                               api_news_creators
 13582  POST             /api/news/creators/generate                      api_news_creators_generate
 13647  POST             /api/news/generate-now                           api_news_generate_now
 13642  GET              /api/news/items                                  api_news_items
 13633  GET              /api/news/preview                                api_news_preview
 13552  GET              /api/news/status                                 api_news_status
 13597  POST             /api/news/toggle                                 api_news_toggle
 16309  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 14646  GET              /api/notify/status                               api_notify_status
 14657  POST             /api/notify/test                                 api_notify_test
 14632  GET              /api/ops/audit                                   api_ops_audit
 16380  GET              /api/ops/db-stats                                api_ops_db_stats
 16408  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 14438  GET              /api/ops/errors                                  api_ops_errors
 16329  GET              /api/ops/healthcheck                             api_ops_healthcheck
 17259  GET              /api/ops/log-tail                                api_ops_log_tail
 12471  GET              /api/ops/logtail                                 api_ops_logtail
 14379  GET              /api/ops/metrics                                 api_ops_metrics
 14362  GET              /api/ops/resource_history                        api_ops_resource_history
 17135  GET              /api/ops/version                                 api_ops_version
 11163  GET              /api/outcomes                                    api_outcomes
 25242  POST             /api/overlay/config                              api_overlay_config
 25229  POST             /api/overlay/event                               api_overlay_event
 25134  GET              /api/overlay/state                               api_overlay_state
 11196  GET              /api/profile/<username>                          api_profile
 15934  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 15756  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 15882  GET              /api/proxy/heatmap                               api_proxy_heatmap
 15859  GET              /api/proxy/trend                                 api_proxy_trend
 13526  GET              /api/public/stats                                api_public_stats
 10758  GET              /api/pulse                                       api_pulse
 15280  GET              /api/recording-attempts                          api_recording_attempts
 23345  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 23323  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 23364  POST             /api/restream/<int:rid>/start                    api_restream_start
 23631  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 25096  GET              /api/restream/chatfeed                           api_restream_chatfeed
 23299  POST             /api/restream/create                             api_restream_create
 13917  GET              /api/restream/deck                               api_restream_deck
 12573  GET              /api/restream/health                             api_restream_health
 25118  POST             /api/restream/layout                             api_restream_layout
 23272  GET              /api/restream/list                               api_restream_list
 12542  POST             /api/restream/report                             api_restream_report
 23644  POST             /api/restream/start_all                          api_restream_start_all
 23670  POST             /api/restream/stop_all                           api_restream_stop_all
 12800  GET              /api/restream/testpush                           api_testpush_status
 12825  POST             /api/restream/testpush                           api_testpush_run
 16717  GET              /api/restream/verify                             api_restream_verify
 14795  GET              /api/retention/preview                           api_retention_preview
 14804  POST             /api/retention/run                               api_retention_run
 25827  POST             /api/schedule/add                                api_schedule_add
 25817  GET              /api/schedule/list                               api_schedule_list
 25852  POST             /api/schedule/remove                             api_schedule_remove
 15633  GET              /api/search                                      api_search
 26385  GET              /api/selftest                                    api_selftest
 23381  GET              /api/shield/stats                                api_shield_stats
 10777  GET              /api/stats                                       api_stats
 15897  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 15824  GET              /api/stats/tiktok-status                         api_tiktok_status
 25792  GET              /api/stats/timeline                              api_stats_timeline
 10854  GET              /api/storage                                     api_storage
 10861  POST             /api/storage/cleanup                             api_storage_cleanup
 15810  GET              /api/stream/inspect/<username>                   api_stream_inspect
 12512  GET              /api/stream/timeline                             api_stream_timeline
 14246  GET              /api/stream/transcript                           api_stream_transcript
 25460  GET              /api/streamer/compare                            api_streamer_compare
 25659  POST             /api/streamer/delete/<username>                  api_streamer_delete
 14756  GET              /api/streamer/detail                             api_streamer_detail
 25684  GET              /api/streamer/digest/<username>                  api_streamer_digest
 25564  GET              /api/streamer/dormant                            api_streamer_dormant
 25640  GET              /api/streamer/exists/<username>                  api_streamer_exists
 25519  GET              /api/streamer/journal/<username>                 api_streamer_journal
 25484  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 25544  GET              /api/streamer/watchlist                          api_streamer_watchlist
 14081  GET              /api/streamers/wall                              api_streamers_wall
 11003  GET              /api/summary/preview                             api_summary_preview
 15345  GET              /api/system                                      api_system
 16665  GET              /api/system/check_timing                         api_check_timing
 17047  GET              /api/system/config_drift                         api_config_drift
 14282  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14493  GET              /api/system/preflight                            api_system_preflight
 14619  GET              /api/system/preflight_history                    api_system_preflight_history
 14929  GET              /api/system/resilience                           api_system_resilience
 15668  GET              /api/tags                                        api_tags_list
 10827  GET              /api/top                                         api_top
 12445  GET              /api/trackings                                   api_trackings
 16198  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 16231  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 15704  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 15917  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 16260  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 15690  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 15119  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 15166  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 15195  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 15177  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 11089  POST             /api/trackings/bulk                              api_trackings_bulk
 15134  GET              /api/trackings/export                            api_trackings_export
 11058  GET              /api/trackings/groups                            api_trackings_groups
 15672  GET              /api/trackings/tags-map                          api_trackings_tags_map
 15972  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11460  GET              /api/trend-7d                                    api_trend_7d
 24130  GET              /api/tts/<fn>                                    api_tts_file
 12680  POST             /api/tunnel/set                                  api_tunnel_set
 12659  GET              /api/tunnel/status                               api_tunnel_status
 12691  POST             /api/tunnel/test                                 api_tunnel_test
 12672  POST             /api/tunnel/toggle                               api_tunnel_toggle
 17019  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 16971  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect
 16995  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 16949  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 17207  GET              /api/update/backups                              api_update_backups
 17173  GET              /api/update/check                                api_update_check
 17232  POST             /api/update/restart                              api_update_restart
 17212  POST             /api/update/rollback                             api_update_rollback
 17195  POST             /api/update/start                                api_update_start
 17188  GET              /api/update/status                               api_update_status
 25270  GET              /api/upload_window                               api_upload_window
 11177  GET              /api/userstats                                   api_userstats
 13658  GET              /api/version                                     api_version
 16811  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 16832  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 16844  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout
 16769  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect
 16793  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 16747  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 30065  GET              /api/youtube/sendrate                            api_youtube_sendrate
 15318  GET              /archive/<int:eid>/download                      archive_download
 15375  GET              /download/<int:recording_id>                     download
 15241  GET              /health                                          health
 23579  GET              /healthz                                         healthz
 10649  GET              /login                                           dashboard_login_page
 10679  GET              /logout                                          dashboard_logout
 10686  GET              /manifest.webmanifest                            pwa_manifest
 14310  GET              /metrics                                         api_prometheus_metrics
 25079  GET              /overlay                                         overlay_page
 10710  GET              /pwa-icon-<variant>.png                          pwa_icon
 10696  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (90)

```
   986  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   726  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   857  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   837  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   875  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   799  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   339  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   350  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   360  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   383  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   390  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   401  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   534  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   632  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1224  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1256  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   323  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   939  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   919  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1092  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1140  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1191  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1050  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   894  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
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
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
```

## Discord-Slash-Commands (45)

```
 27090  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 27549  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 27181  /assign_role            Rolle/Gruppe einem Mitglied geben
 27227  /ban                    Mitglied bannen
 27881  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 27805  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 27845  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 27830  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 27672  /clips                  Letzte Highlight-Clips eines Users
 27142  /create_category        Kategorie anlegen
 27111  /create_channel         Text-Channel anlegen (optional in Kategorie)
 27170  /create_group           Nutzergruppe (= Rolle) anlegen
 27153  /create_role            Rolle / Nutzergruppe anlegen
 27127  /create_voice           Voice-Channel anlegen
 27463  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 27579  /event                  Community-Event ankündigen (Admin) — mit Countdown
 27622  /events                 Kommende Community-Events anzeigen
 27718  /follow                 Bei Live-Gang eines Streamers gepingt werden
 27702  /help                   Alle Bot-Befehle anzeigen
 27216  /kick                   Mitglied kicken
 27445  /leaderboard            Top-10 der Community nach XP
 27658  /livenow                Welche getrackten User sind gerade live
 27688  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 27519  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 27251  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 27431  /rank                   Dein Level und Rang anzeigen
 27645  /recstatus              Aktuell laufende Aufnahmen
 27192  /remove_role            Rolle/Gruppe entfernen
 27104  /restream_status        Restream-Status
 27203  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 27396  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 27414  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 27744  /stats                  Statistik zu einem getrackten Streamer
 27016  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 28040  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 27937  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 27913  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 27238  /timeout                Mitglied stummschalten (Minuten)
 27816  /topstreamers           Rangliste der Streamer nach Aufnahmen
 27046  /track                  TikTok-User tracken
 27030  /tracklist              Getrackte TikTok-User dieses Servers
 27733  /unfollow               Live-Pings für einen Streamer abbestellen
 27079  /untrack                TikTok-User nicht mehr tracken
 27766  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 27790  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 28524  on_member_join
 28486  on_message
 28127  on_raw_reaction_add
 28559  on_ready
```

## Top-Level-Symbole in bot.py (565 Funktionen, 2 Klassen)

```
  2469-2470   _abo_key
  2490-2508   _abo_probe_dump
 25927-25937  _active_recorder_sync
 20569-20576  _ad_allowlist
 21691-21697  _agent_for
 25939-25957  _ai_calls_total_sync
 21700-21716  _ai_telemetry
 22198-22216  _alert
 28672-28722  _alert_monitor_loop
 29096-29158  _announce_loop
  3411-3414   _anthropic_key
  3421-3423   _anthropic_model
 10406-10409  _arg_int
  2461-2466   _as_dict
 18429-18434  _audio_cfg
 22352-22374  _audio_tap_cmd
 10570-10581  _auth_cookie
 10537-10566  _auth_guard
  1617-1622   _auto_on
 23248-23266  _auto_restream_loop
 30226-30241  _azrael_broadcast_reply
 30126-30148  _azrael_chat_reply
 30109-30123  _azrael_chat_should_reply
 13252-13270  _azrael_creator_take
 30154-30156  _azrael_gate_cfg
 21721-21735  _azrael_live_state
 24978-24992  _azrael_overlay_state
 22081-22135  _azrael_proactive_loop
 21540-21596  _azrael_reaction_to_chats
 30159-30166  _azrael_reply_all_chats
 30096-30106  _azrael_self_names
 30194-30223  _azrael_send_to
 21738-21759  _azrael_system
 28836-28839  _backup_active
 28917-28930  _backup_loop
 20457-20458  _badwords_path
 28637-28646  _brain_growth_loop
 11536-11563  _brain_growth_snapshot
  2397-2417   _brain_hint_delay
 11528-11530  _brain_history_for
  6833-6861   _brain_notify
 11505-11526  _brain_record
 11532-11534  _brain_stream_recent
 14843-14860  _browser_push
  6877-6964   _build_daily_summary
  2900-3080   _build_native_cmd
 18777-18964  _build_restream_cmd
  3124-3157   _build_ytdlp_cmd
 25879-25886  _cached_probe
  5655-5682   _can_stop_tracking
  1797-1819   _capture_set_cookies
 16020-16023  _cfg_get
 16026-16028  _cfg_set
 24722-24757  _channel_set_all
 18027-18030  _chat_connected
 18033-18049  _chat_disconnected
  8907-8918   _chat_is_forum
 18069-18071  _chat_sanitize
 18073-18082  _chat_src_ok
 18012-18024  _chat_stat
 18052-18055  _chat_stats_snapshot
  3686-3697   _check_ai_alive_sync
  3700-3712   _check_ai_models_sync
 25888-25901  _check_redis_alive_sync
 25903-25923  _check_redis_version_sync
 14721-14734  _ci_key
 12135-12178  _classify_pool_anonymity
 12181-12198  _classify_pool_anonymity_bg
   775-779    _claude_chat_sync_metered
 10431-10438  _client_ip
 29190-29217  _clip_prune
 29220-29230  _clip_recfile_for
 29746-29752  _clip_should_velocity
 29271-29353  _clip_to_discord
  3584-3593   _close_ai_session
 30270-30285  _cohost_broadcast
 30252-30256  _cohost_cfg
 30311-30323  _cohost_fire_highlight
 30259-30267  _cohost_gate
 30288-30308  _cohost_highlight
 29402-29436  _community_events_loop
 11359-11361  _conv_messages
  7257-7297   _cookie_alarm_loop
  1869-1873   _cookie_autorefresh_info
  1774-1778   _cookie_header
 14893-14925  _cpu_load_snapshot
  3894-3906   _create_index_safe
 13220-13235  _creator_activity
 13276-13299  _creator_dossier_generate
 13238-13249  _creator_facts_line
 26140-26246  _crowdsec_status
 26106-26137  _crowdsec_via_lapi
 25971-25989  _cscli_bin
 25995-26008  _cscli_path
  7150-7175   _daily_summary_loop
 26026-26043  _darf_journal_lesen
 11026-11054  _dashboard_track_group
 28649-28669  _db_maintenance_loop
  7122-7147   _db_vacuum_loop
 20592-20616  _detect_foreign_ad
  1356-1367   _diag_path_owner
 21987-22031  _director_finalize
 22798-22805  _director_for
 21936-21984  _director_mark
 29640-29675  _disc_automod_check
 29613-29619  _disc_state_get
 29622-29629  _disc_state_set
 26689-26702  _discord_guild_filesize_bytes
 26888-26897  _discord_invite
 29574-29610  _discord_live_thread
 22138-22150  _discord_notify
 26789-26814  _discord_ops_alert
 29472-29570  _discord_post_user
 26953-28634  _discord_run_once
 26827-26885  _discord_start
 29161-29167  _discord_stop
 26710-26712  _discord_upload_limit_label
 26705-26707  _discord_upload_limit_mb
  7178-7252   _disk_alarm_loop
 31652-31701  _disk_autoclean
 31704-31717  _disk_guard_loop
 31644-31649  _disk_pct
 25035-25038  _donations_unknown_count
 18386-18388  _drawtext_chain
 15472-15474  _dump_all_threads
 12060-12124  _enrich_proxies_with_geo
  2014-2058   _ensure_cookie_file_netscape
 26900-26950  _ensure_discord_invite
 29367-29399  _ensure_error_channel
  8966-8969   _ensure_notify_topic
 12303-12340  _ensure_proxy_ready
  8920-8947   _ensure_topic
   638-640    _env_int
   643-645    _env_int_range
 29439-29469  _error_channel_loop
 22182-22195  _event_webhook
 17320-17326  _evo_build_dir
 17329-17336  _evo_version
 17612-17693  _evolution_cycle
 17345-17365  _evolution_llm_note
 17696-17706  _evolution_loop
 17368-17609  _evolution_write_build
  6275-6309   _extract_file_payload
  2146-2148   _extract_urls_from_streamurl_node
 26011-26018  _f2b_sudo_hint
 22218-22220  _faster_whisper_available
 20481-20493  _fetch_ldnoobw_de
 11949-11967  _fetch_proxy_list
 22632-22660  _fetch_tiktok_room_id
   709-712    _ff_cmd
 16143-16156  _ffmpeg_version_str
 18549-18554  _find_chromium
  3117-3121   _find_external_recorder
  2151-2153   _find_stream_urls
 16071-16096  _fire_webhooks
  8033-8042   _fork_safe
   790-799    _freeai_chat_sync_metered
 26061-26103  _geo_lookup_ips
  3573-3582   _get_ai_session
  7867-7907   _get_live_info
  2687-2694   _get_resolve_semaphore
  8268-8634   _handle_single_tracking
 31496-31498  _hb
 31501-31518  _hb_while
 18087-18089  _highlight_cfg
 18092-18121  _highlight_observe
 18557-18562  _htmlov_screenshot_cmd
 22376-22386  _httpx_proxy
 16104-16116  _in_quiet_hours
 32531-32562  _install_fast_eventloop
 10301-10355  _install_fast_json
 15477-15493  _install_faulthandler
 23491-23500  _intel_ensure_schema
 23538-23569  _intel_index_loop
 23512-23522  _intel_index_one
 23503-23509  _intel_semantic
  5644-5653   _is_authorized
  8198-8204   _is_dead
  2136-2138   _is_hevc
 26046-26052  _is_private_ip
  1520-1527   _is_process_running
  6863-6874   _is_quiet_hours
  1160-1169   _is_upload_window
 10390-10403  _json_error_handler
  7080-7110   _kick_broadcaster_id
 12726-12745  _kick_channel_live
  6997-7039   _kick_follower_count
 13804-13817  _kick_oauth_exchange
 13820-13822  _kick_oauth_page
 13763-13767  _kick_redirect_public
 13758-13760  _kick_redirect_source
 13750-13755  _kick_redirect_uri
  6982-6984   _kick_slug
 13770-13801  _kick_user_token
  3943-3946   _kind_from_filename
 16133-16138  _latest_popularity
 20503-20509  _learned_load
 20500-20501  _learned_path
 20511-20519  _learned_save
 23013-23043  _live_react_loop
 22809-23002  _live_react_worker
 21599-21610  _live_transcript_push
 23004-23011  _live_users
 22034-22078  _living_title_loop
 20460-20468  _load_banned_words_file
  1695-1768   _load_cookies_dict
 28842-28914  _local_backup_scan
 10372-10386  _log_5xx
 18972-18984  _looks_like_codec_err
 18967-18969  _looks_like_source_expired
  8114-8144   _loop_fehler
 15497-15506  _loop_heartbeat
 31466-31493  _loop_lag_monitor
 15616-15619  _loop_not_ready
 15509-15577  _loop_watchdog_thread
 21479-21493  _loyalty_add
 21470-21476  _loyalty_get
 21496-21504  _loyalty_top
 16517-16535  _manual_donations_rows
 16538-16540  _manual_donations_total
  8206-8207   _mark_dead
 12893-12922  _marketing_cfg
 12884-12890  _marketing_default_targets
 12879-12881  _marketing_enabled
 12936-12951  _marketing_flavor
 13006-13022  _marketing_loop
 12954-12964  _marketing_post_discord
 12967-12979  _marketing_post_telegram
 12982-13003  _marketing_publish
 12925-12929  _marketing_state_obj
 12932-12933  _marketing_state_save
 30173-30191  _maybe_handle_command
 31803-31827  _maybe_hype_clip
  3861-3884   _migrate_columns
 30450-30461  _mod_is_exempt
 30464-30469  _mod_warn_first
 30472-30475  _mod_warn_text
 17875-17883  _modlog
   913-915    _multistream_targets
  8045-8046   _nc_create_subprocess_exec
  8049-8050   _nc_create_subprocess_shell
 13117-13133  _news_cfg
 13104-13106  _news_enabled
 13171-13212  _news_facts
 13326-13348  _news_generate
 13531-13548  _news_loop
 13109-13114  _news_output_path
 13215-13217  _news_phrase
 13302-13323  _news_phrase_impl
 13146-13153  _news_read
 13136-13139  _news_state_obj
 13142-13143  _news_state_save
 13156-13168  _news_write
 17913-17915  _normalize_ingest
  2328-2345   _note_check_duration
  8960-8963   _notify_topic_name
 13714-13725  _oauth_redirect_env
 13741-13747  _oauth_redirect_source
 13728-13738  _oauth_redirect_uri
 21625-21633  _oracle_memories
 21891-21925  _oracle_memorize
 21636-21649  _oracle_persona
 21618-21622  _oracle_recent_text
 18212-18220  _ov_atomic_write
 18200-18206  _ov_bar
 20416-20428  _ov_clip_text
 18209-18210  _ov_oneline
 25046-25075  _overlay_push
 18503-18546  _overlay_render_size
 17974-17978  _overlay_session_reset
 24994-24997  _overlay_src_ok
 20579-20589  _own_invites
 16498-16514  _parse_eur
 18498-18500  _parse_size
 26254-26334  _parse_ssh_attacks
  7469-7502   _pause_resume_cmd
  1823-1867   _persist_refreshed_cookies
  1661-1693   _pick_checked_pull_proxy
 10467-10480  _pin_auth_value
 10526-10527  _pin_clear_fail
 10506-10509  _pin_locked
 10512-10523  _pin_note_fail
 10483-10503  _pin_ok
 24884-24886  _piper_available
 24849-24871  _piper_list_voices
 24891-24916  _piper_pick_model
 24928-24975  _piper_say
 24842-24846  _piper_voice_roots
 16033-16068  _post_json_threaded
 18477-18495  _probe_video_size
  1548-1565   _proc_is_recorder
 12047-12058  _proxy_geo_cache_put
 12274-12300  _proxy_pool_refresh_loop
  1627-1658   _proxy_report_recording
 15462-15464  _prune_stall_dumps
 13673-13711  _public_base_url
 13351-13472  _public_stats
 22153-22179  _push_notify
 10628-10630  _pwa_dir
 12018-12033  _quick_validate_proxy
 16099-16101  _quiet_hours_config
 10593-10626  _rate_guard
 21444-21450  _react_warn
  7953-7992   _reap_proc
  2368-2390   _record_check_outcome
   704-706    _redact_stream_urls
 12201-12271  _refresh_proxy_pool
 24874-24880  _resolve_piper_model
 14737-14752  _resolve_tracked_user
  2162-2252   _resolve_via_html
  2510-2664   _resolve_via_webcast_api_v2
  2727-2789   _resolve_via_ytdlp
 29792-29921  _resolve_youtube_ingest
 23082-23089  _restream_active_platforms
 17959-17970  _restream_active_sources
 22663-22762  _restream_chat_guardian
 18124-18196  _restream_chat_push
 17886-17898  _restream_enabled
 18565-18652  _restream_html_overlay_start
 18655-18668  _restream_html_overlay_stop
  1108-1110   _restream_layout_mode
 17924-17947  _restream_overlay_files
 23047-23079  _restream_platform_state
 23210-23245  _restream_resume_after_restart
 18716-18774  _restream_tts_enqueue_wav
 18439-18471  _restream_tts_feeder
 18436-18437  _restream_tts_fifo_path
 18671-18698  _restream_tts_start
 18700-18714  _restream_tts_stop
 23092-23207  _restream_verify_loop
 28807-28819  _retention_loop
 28766-28804  _retention_scan
  2472-2474   _room_is_abo
  6313-6430   _run_ai_call
 15600-15613  _run_async_from_flask
 26055-26058  _run_priv
 32519-32527  _run_selfcheck_and_exit
 28822-28833  _s3_client
  8209-8255   _safe_send
  4796-4812   _sample_net_throughput
 20470-20478  _save_banned_words_file
  2420-2447   _schedule_next_check
 28725-28763  _scheduler_loop
  3887-3891   _schema_pk
 15621-15626  _scraper_session
 30478-30517  _screen_full
 14130-14167  _sec_headers
  2141-2143   _select_stream_from_data_section
 32332-32516  _selfcheck
  8972-9006   _send_live_notice
  1183-1187   _should_defer_upload
 29233-29268  _shrink_for_discord
 10633-10645  _sicheres_ziel
 31724-31741  _sign_health_check
 31744-31763  _sign_health_loop
  8062-8073   _spawn
  8076-8106   _spawn_from_flask
 26378-26381  _st_befund
 22388-22629  _start_chat_listener
 15580-15597  _start_loop_watchdog
 13496-13522  _stats_loop
 13475-13478  _stats_output_path
 13481-13493  _stats_write
  8702-8716   _storage_cleanup_loop
 31783-31790  _story_for
  3179-3185   _stream_url_expiry
  3194-3200   _stream_url_is_fresh
  3187-3192   _stream_url_ttl
 20543-20550  _streamer_persona_get
 20525-20531  _streamer_personas_load
 20522-20523  _streamer_personas_path
 20533-20541  _streamer_personas_save
 18391-18395  _studio_chain
 28939-29061  _system_backup
 29064-29092  _system_backup_loop
 11970-12009  _test_proxy
 12767-12776  _testpush_cfg
 12779-12796  _testpush_exec
 12748-12764  _testpush_resolve_live
  8879-8889   _tg_topics_load_into_mem
  8876-8877   _tg_topics_path
  8891-8898   _tg_topics_save
 25588-25636  _tiktok_account_exists
 10441-10449  _token_ok
  8901-8905   _topic_forget
 16119-16130  _tracking_max_duration
  1414-1437   _try_attach_file_handler
 24918-24926  _tts_cleanup
 12652-12655  _tunnel_effective
 24344-24397  _twitch_channel_status
 30520-30663  _twitch_chat_loop
 30334-30437  _twitch_eventsub_loop
 17040-17043  _twitch_oauth_page
  1206-1219   _upload_queue_add
  1230-1232   _upload_queue_count
  1189-1198   _upload_queue_load
  1179-1181   _upload_queue_path
  1221-1228   _upload_queue_remove
  1200-1204   _upload_queue_save
  1234-1272   _upload_window_loop
  7926-7933   _uptime_s
 17901-17910  _url_host
   684-701    _url_ohne_zugang
   768-772    _usage_record_claude
  8147-8191   _verbindung_verloren
  7042-7070   _viewer_sample_loop
  7112-7119   _viewer_stats
 10530-10533  _wants_html
  7936-7950   _warn_empty_env
 31539-31634  _watchdog_loop
 30075-30083  _wchat_thank_ok
 22222-22252  _whisper_get_model
  8023-8030   _whisper_native_section
 21431-21437  _whisper_pool
 22321-22350  _whisper_segments
 22254-22318  _whisper_transcribe
 18222-18384  _write_restream_overlay
 30691-30764  _youtube_api_chat_loop
 24400-24503  _youtube_api_status
 24506-24573  _youtube_channel_status
 30767-30924  _youtube_chat_loop
 29927-29940  _youtube_restream_autoconfig
 29943-29967  _youtube_restream_autoconfig_inner
 30033-30061  _youtube_send
 24678-24719  _youtube_set_channel
 29970-30004  _yt_access_token
 30007-30022  _yt_live_chat_id
 30684-30688  _yt_oauth_configured
 30028-30030  _yt_sendrate_cfg
 30666-30681  _yt_timeout
  2711-2712   _ytdlp_detect_available
  2714-2725   _ytdlp_note_result
 15467-15469  _zombie_child_count
  7803-7827   about
  4062-4066   add_ai_log_entry
  3979-3982   add_archive_entry
  4909-4924   add_archive_rule
  4491-4525   add_recording
  4152-4169   add_tracking
  4586-4603   add_tracking_tag
  6433-6466   ai
  3726-3765   ai_chat
  3799-3809   ai_history_append
  3811-3816   ai_history_clear
  3788-3797   ai_history_load
  3773-3786   ai_rate_limit_check
  6495-6503   aireset
 21762-21781  azrael_chat
 30929-31051  brain_cmd
  3203-3387   build_recording_cmd
  4172-4249   bulk_add_trackings
  7300-7359   bulkadd
  8719-8859   check_all_trackings
  4336-4348   claim_live_transition
 20619-21374  class KickModerator
 18987-20303  class RestreamManager
 12385-12427  classify_proxy_anonymity
  6541-6739   cleanup
  5504-5545   cleanup_old_recordings
  4482-4489   clear_recording
 29678-29743  clip_moment
  5057-5100   cluster_failures
  4740-4789   compute_storage_forecast
  7422-7466   cookies_cmd
  5346-5352   cookies_days_old
  4143-4149   count_trackings_for_chat
  4049-4060   decide_preferred_recorder
  3989-3992   delete_archive_entry
  4926-4934   delete_archive_rule
  5970-6117   diag
 31163-31224  einnahmen_cmd
  4734-4737   find_recordings_by_fingerprint
  4010-4026   finish_recording_attempt
  4281-4291   get_all_active_trackings
  4088-4091   get_all_checks
  4527-4530   get_all_recordings
  4628-4638   get_all_tags_with_counts
  4711-4714   get_annotations_for_recording
  3984-3987   get_archive_entry
  4704-4707   get_bookmarked_recordings
  1890-2007   get_cookie_health
  4577-4583   get_event_log
  4033-4047   get_last_recording_attempt
  2792-2897   get_live_status
  5260-5263   get_manual_recordings
  4719-4722   get_or_compute_inspect_sync
  5580-5624   get_outcome_breakdown
  4685-4693   get_priority_poll_interval
  4887-4896   get_profile_snapshots
  4068-4078   get_recent_ai_log
  4028-4031   get_recent_recording_attempts
  4532-4535   get_recording_by_id
  4697-4700   get_recording_note
  3521-3544   get_redis
  4119-4135   get_stats
  5471-5502   get_storage_stats
  4618-4626   get_tags_for_tracking
  5027-5041   get_tiktok_status_distribution
  4672-4683   get_tracking_priority
  4350-4359   get_tracking_state
  4277-4279   get_trackings_for_group
  5276-5279   get_trash_recordings
  9627-10269  handle_recording_finished
  3909-3934   init_db
  5394-5448   inspect_stream_url
 25041-25043  is_revenue_platform
  4899-4907   list_archive_rules
  5774-5812   live
  8258-8266   live_check_worker
  3596-3630   llm_chat
  3653-3681   llm_chat_sync
  3638-3650   llm_list_models
  4543-4569   log_event
  1482-1515   log_recording_failure
  7616-7665   logs_cmd
 31831-32322  main
  6469-6492   on_ai_media
  7742-7768   on_ai_reply
  7771-7800   on_azrael_mention
  7832-7862   on_callback
 21784-21888  oracle_handle
  7505-7508   pause_tracking
  5634-5639   profile_keyboard
  5355-5391   quick_restart_tracking
  7567-7613   quota
  8636-8699   reaper_loop
  5023-5025   record_tiktok_status
  6508-6538   recstatus
  3546-3554   redis_get_json
  3556-3562   redis_set_json
  4251-4275   remove_tracking
  4605-4616   remove_tracking_tag
 31227-31237  report_cmd
 12430-12432  report_proxy_result
  2255-2282   resolve_tiktok_live_stream
  5271-5274   restore_recording
  7511-7514   resume_tracking
  4937-5017   run_archive_rules
 31240-31446  run_bot
 15389-15436  run_flask
  4815-4860   sample_bandwidth_for_active
  4866-4885   save_profile_snapshot
  4080-4086   save_tiktok_check
  4474-4480   set_recording_file
  4294-4332   set_tracking_paused
  4641-4670   set_tracking_priority
  5266-5269   soft_delete_recording
  9012-9625   split_and_send_video
  5687-5729   start
  3994-4008   start_recording_attempt
  6742-6780   stats
  5241-5258   stop_manual_recording
  7517-7564   stoprec
  6967-6975   summary_cmd
  7668-7739   sysres
  6119-6263   teststream
  5731-5772   tiktok
  7362-7419   topusers
  5849-5906   track
  5814-5846   track_exact
  5920-5968   tracklist
  5107-5239   trigger_manual_recording
  4435-4472   try_acquire_recording_lock
  5282-5341   universal_search
  5908-5918   untrack
 31054-31160  update_cmd
  4729-4732   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
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
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
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
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
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
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
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
