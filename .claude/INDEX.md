# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot_v37.py (261)

```
 10655  GET              /                                                dashboard
 15545  GET              /api/abo/status                                  api_abo_status
 10754  GET              /api/active-recordings                           api_active_recordings
 15620  GET              /api/activity-pulse                              api_activity_pulse
 14973  GET              /api/ai-log                                      api_ai_log
 11152  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 15380  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 23429  GET/POST         /api/audio/config                                api_audio_config
 23459  POST             /api/audio/testtone                              api_audio_testtone
 15486  GET/POST         /api/auto-archive-rules                          api_archive_rules
 15510  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 15514  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12430  GET              /api/automation/status                           api_automation_status
 12452  POST             /api/automation/toggle                           api_automation_toggle
 14178  GET              /api/azrael/agents                               api_azrael_agents
 12333  POST             /api/azrael/ask                                  api_azrael_ask
 23665  GET/POST         /api/azrael/context                              api_azrael_context
 13805  GET              /api/azrael/core                                 api_azrael_core
 23799  POST             /api/azrael/live_pause                           api_azrael_live_pause
 23789  GET              /api/azrael/live_status                          api_azrael_live_status
 23807  POST             /api/azrael/live_test                            api_azrael_live_test
 14187  GET              /api/azrael/memories                             api_azrael_memories
 23855  POST             /api/azrael/persona                              api_azrael_persona_set
 23846  GET              /api/azrael/personas                             api_azrael_personas
 23883  GET              /api/azrael/piper_status                         api_azrael_piper_status
 23638  POST             /api/azrael/react                                api_azrael_react
 23674  GET              /api/azrael/reaction                             api_azrael_reaction
 23826  GET              /api/azrael/reactions                            api_azrael_reactions
 23876  GET              /api/azrael/transcript                           api_azrael_transcript
 23761  POST             /api/azrael/tts_test                             api_azrael_tts_test
 23736  GET              /api/azrael/voices                               api_azrael_voices
 23900  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11247  GET              /api/backoff-watch                               api_backoff_watch
 14744  POST             /api/backup/run                                  api_backup_run
 14710  GET              /api/backup/status                               api_backup_status
 14699  POST             /api/backup/system                               api_backup_system
 15452  GET              /api/bandwidth/live                              api_bandwidth_live
 15365  GET              /api/bookmarks                                   api_bookmarks_list
 11510  GET              /api/brain                                       api_brain
 11447  GET              /api/brain/alarms                                api_brain_alarms
 11432  GET              /api/brain/creator                               api_brain_creator
 11409  GET              /api/brain/graph                                 api_brain_graph
 11470  GET              /api/brain/growth                                api_brain_growth
 10209  GET              /api/brain/health                                api_brain_health
 24381  GET              /api/channel/categories                          api_channel_categories
 24387  POST             /api/channel/set                                 api_channel_set
 24197  GET              /api/channels/status                             api_channels_status
 23030  POST             /api/chat/send                                   api_chat_send
 14445  GET              /api/chat/send_status                            api_chat_send_status
 10735  GET              /api/checks                                      api_checks
 23702  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 23685  GET              /api/clips                                       api_clips
 23718  POST/DELETE      /api/clips/clear                                 api_clips_clear
 23304  GET              /api/cohost                                      api_cohost
 23316  POST             /api/cohost/config                               api_cohost_config
 16184  GET              /api/community/stats                             api_community_stats
 25381  POST             /api/config/restore                              api_config_restore
 25366  GET              /api/config/snapshot                             api_config_snapshot
 15643  GET              /api/cookies/age                                 api_cookies_age
 10802  GET              /api/cookies/health                              api_cookies_health
 10809  POST             /api/cookies/update                              api_cookies_update
 25332  GET              /api/data/export                                 api_data_export
 16699  GET              /api/db/export                                   api_db_export
 16726  POST             /api/db/import                                   api_db_import
 16686  GET              /api/db/summary                                  api_db_summary
 23230  GET              /api/debug/threads                               api_debug_threads
 26267  GET              /api/defense/attacks                             api_defense_attacks
 26234  GET              /api/defense/crowdsec                            api_defense_crowdsec
 26252  GET              /api/defense/fail2ban                            api_defense_fail2ban
 25958  GET              /api/defense/overview                            api_defense_overview
 14806  POST             /api/discord/announce                            api_discord_announce
 14534  GET              /api/discord/clips_week                          api_discord_clips_week
 14750  GET              /api/discord/community                           api_discord_community
 14473  GET              /api/discord/invite                              api_discord_invite
 13936  GET              /api/discord/overview                            api_discord_overview
 14022  POST             /api/discord/webhook_test                        api_discord_webhook_test
 16261  POST             /api/donations/add                               api_donations_add
 16294  GET              /api/donations/manual                            api_donations_manual
 16302  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 16197  POST             /api/donations/reset                             api_donations_reset
 16318  GET              /api/donations/summary                           api_donations_summary
 15434  GET              /api/events                                      api_events
 14581  GET              /api/events/stream                               api_events_stream
 17452  GET              /api/evolution/changelog                         api_evolution_changelog
 17437  GET              /api/evolution/history                           api_evolution_history
 17377  GET              /api/evolution/learned                           api_evolution_learned
 17399  GET              /api/evolution/proposals                         api_evolution_proposals
 17420  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 17367  POST             /api/evolution/run                               api_evolution_run
 17467  GET              /api/evolution/snapshots                         api_evolution_snapshots
 17332  GET              /api/evolution/status                            api_evolution_status
 16533  GET              /api/finanzamt/entries                           api_finanzamt_entries
 16553  POST             /api/finanzamt/entry                             api_finanzamt_add
 16580  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 15447  GET              /api/forecast/storage                            api_forecast_storage
 12468  GET              /api/freeai/status                               api_freeai_status
 13878  GET              /api/health                                      api_health
 15465  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 15461  GET              /api/heatmap/recordings                          api_heatmap_recordings
 23353  GET              /api/highlights                                  api_highlights
 23365  POST             /api/highlights/config                           api_highlights_config
 24238  GET              /api/kick/channel                                api_kick_channel
 24259  POST             /api/kick/channel                                api_kick_channel_set
 13605  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 13673  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 13651  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 13590  GET              /api/kick/oauth/start                            api_kick_oauth_start
 13630  GET              /api/kick/oauth/status                           api_kick_oauth_status
 23477  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 23546  POST             /api/kickmod/config                              api_kickmod_config
 23591  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 23605  GET              /api/kickmod/learned                             api_kickmod_learned
 23632  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 23612  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 23943  POST             /api/kickmod/say                                 api_kickmod_say
 23919  POST             /api/kickmod/start                               api_kickmod_start
 23517  GET              /api/kickmod/status                              api_kickmod_status
 23930  POST             /api/kickmod/stop                                api_kickmod_stop
 10589  POST             /api/login                                       dashboard_login_submit
 16169  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 12883  POST             /api/marketing/config                            api_marketing_config
 12908  GET              /api/marketing/preview                           api_marketing_preview
 12918  POST             /api/marketing/send-now                          api_marketing_send_now
 12857  GET              /api/marketing/status                            api_marketing_status
 12875  POST             /api/marketing/toggle                            api_marketing_toggle
 23380  GET              /api/moderation/feed                             api_moderation_feed
 13436  POST             /api/news/config                                 api_news_config
 13402  GET              /api/news/creators                               api_news_creators
 13413  POST             /api/news/creators/generate                      api_news_creators_generate
 13478  POST             /api/news/generate-now                           api_news_generate_now
 13473  GET              /api/news/items                                  api_news_items
 13464  GET              /api/news/preview                                api_news_preview
 13383  GET              /api/news/status                                 api_news_status
 13428  POST             /api/news/toggle                                 api_news_toggle
 16026  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 14410  GET              /api/notify/status                               api_notify_status
 14421  POST             /api/notify/test                                 api_notify_test
 14396  GET              /api/ops/audit                                   api_ops_audit
 16097  GET              /api/ops/db-stats                                api_ops_db_stats
 16125  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 14202  GET              /api/ops/errors                                  api_ops_errors
 16046  GET              /api/ops/healthcheck                             api_ops_healthcheck
 16879  GET              /api/ops/log-tail                                api_ops_log_tail
 12313  GET              /api/ops/logtail                                 api_ops_logtail
 14143  GET              /api/ops/metrics                                 api_ops_metrics
 14126  GET              /api/ops/resource_history                        api_ops_resource_history
 16755  GET              /api/ops/version                                 api_ops_version
 11005  GET              /api/outcomes                                    api_outcomes
 24862  POST             /api/overlay/config                              api_overlay_config
 24849  POST             /api/overlay/event                               api_overlay_event
 24754  GET              /api/overlay/state                               api_overlay_state
 11038  GET              /api/profile/<username>                          api_profile
 15651  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 15473  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 15599  GET              /api/proxy/heatmap                               api_proxy_heatmap
 15576  GET              /api/proxy/trend                                 api_proxy_trend
 13357  GET              /api/public/stats                                api_public_stats
 10689  GET              /api/pulse                                       api_pulse
 14997  GET              /api/recording-attempts                          api_recording_attempts
 22965  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 22943  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 22984  POST             /api/restream/<int:rid>/start                    api_restream_start
 23251  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 24716  GET              /api/restream/chatfeed                           api_restream_chatfeed
 22919  POST             /api/restream/create                             api_restream_create
 13681  GET              /api/restream/deck                               api_restream_deck
 12404  GET              /api/restream/health                             api_restream_health
 24738  POST             /api/restream/layout                             api_restream_layout
 22892  GET              /api/restream/list                               api_restream_list
 12377  POST             /api/restream/report                             api_restream_report
 23264  POST             /api/restream/start_all                          api_restream_start_all
 23290  POST             /api/restream/stop_all                           api_restream_stop_all
 12631  GET              /api/restream/testpush                           api_testpush_status
 12656  POST             /api/restream/testpush                           api_testpush_run
 16434  GET              /api/restream/verify                             api_restream_verify
 14512  GET              /api/retention/preview                           api_retention_preview
 14521  POST             /api/retention/run                               api_retention_run
 25447  POST             /api/schedule/add                                api_schedule_add
 25437  GET              /api/schedule/list                               api_schedule_list
 25472  POST             /api/schedule/remove                             api_schedule_remove
 15350  GET              /api/search                                      api_search
 26005  GET              /api/selftest                                    api_selftest
 23001  GET              /api/shield/stats                                api_shield_stats
 10708  GET              /api/stats                                       api_stats
 15614  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 15541  GET              /api/stats/tiktok-status                         api_tiktok_status
 25412  GET              /api/stats/timeline                              api_stats_timeline
 10776  GET              /api/storage                                     api_storage
 10783  POST             /api/storage/cleanup                             api_storage_cleanup
 15527  GET              /api/stream/inspect/<username>                   api_stream_inspect
 12354  GET              /api/stream/timeline                             api_stream_timeline
 14010  GET              /api/stream/transcript                           api_stream_transcript
 25080  GET              /api/streamer/compare                            api_streamer_compare
 25279  POST             /api/streamer/delete/<username>                  api_streamer_delete
 14486  GET              /api/streamer/detail                             api_streamer_detail
 25304  GET              /api/streamer/digest/<username>                  api_streamer_digest
 25184  GET              /api/streamer/dormant                            api_streamer_dormant
 25260  GET              /api/streamer/exists/<username>                  api_streamer_exists
 25139  GET              /api/streamer/journal/<username>                 api_streamer_journal
 25104  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 25164  GET              /api/streamer/watchlist                          api_streamer_watchlist
 13845  GET              /api/streamers/wall                              api_streamers_wall
 10925  GET              /api/summary/preview                             api_summary_preview
 15062  GET              /api/system                                      api_system
 16382  GET              /api/system/check_timing                         api_check_timing
 16667  GET              /api/system/config_drift                         api_config_drift
 14046  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14257  GET              /api/system/preflight                            api_system_preflight
 14383  GET              /api/system/preflight_history                    api_system_preflight_history
 14646  GET              /api/system/resilience                           api_system_resilience
 15385  GET              /api/tags                                        api_tags_list
 10749  GET              /api/top                                         api_top
 12287  GET              /api/trackings                                   api_trackings
 15915  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 15948  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 15421  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 15634  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 15977  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 15407  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 14836  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 14883  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 14912  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 14894  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 10942  POST             /api/trackings/bulk                              api_trackings_bulk
 14851  GET              /api/trackings/export                            api_trackings_export
 15389  GET              /api/trackings/tags-map                          api_trackings_tags_map
 15689  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11302  GET              /api/trend-7d                                    api_trend_7d
 23750  GET              /api/tts/<fn>                                    api_tts_file
 12511  POST             /api/tunnel/set                                  api_tunnel_set
 12490  GET              /api/tunnel/status                               api_tunnel_status
 12522  POST             /api/tunnel/test                                 api_tunnel_test
 12503  POST             /api/tunnel/toggle                               api_tunnel_toggle
 16639  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 16616  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 16598  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 16827  GET              /api/update/backups                              api_update_backups
 16793  GET              /api/update/check                                api_update_check
 16852  POST             /api/update/restart                              api_update_restart
 16832  POST             /api/update/rollback                             api_update_rollback
 16815  POST             /api/update/start                                api_update_start
 16808  GET              /api/update/status                               api_update_status
 24890  GET              /api/upload_window                               api_upload_window
 11019  GET              /api/userstats                                   api_userstats
 13489  GET              /api/version                                     api_version
 16495  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 16516  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 16480  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 16464  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 29685  GET              /api/youtube/sendrate                            api_youtube_sendrate
 15035  GET              /archive/<int:eid>/download                      archive_download
 15092  GET              /download/<int:recording_id>                     download
 14958  GET              /health                                          health
 23199  GET              /healthz                                         healthz
 10580  GET              /login                                           dashboard_login_page
 10610  GET              /logout                                          dashboard_logout
 10617  GET              /manifest.webmanifest                            pwa_manifest
 14074  GET              /metrics                                         api_prometheus_metrics
 24699  GET              /overlay                                         overlay_page
 10641  GET              /pwa-icon-<variant>.png                          pwa_icon
 10627  GET              /sw.js                                           pwa_service_worker
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
 26710  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 27169  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 26801  /assign_role            Rolle/Gruppe einem Mitglied geben
 26847  /ban                    Mitglied bannen
 27501  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 27425  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 27465  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 27450  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 27292  /clips                  Letzte Highlight-Clips eines Users
 26762  /create_category        Kategorie anlegen
 26731  /create_channel         Text-Channel anlegen (optional in Kategorie)
 26790  /create_group           Nutzergruppe (= Rolle) anlegen
 26773  /create_role            Rolle / Nutzergruppe anlegen
 26747  /create_voice           Voice-Channel anlegen
 27083  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 27199  /event                  Community-Event ankündigen (Admin) — mit Countdown
 27242  /events                 Kommende Community-Events anzeigen
 27338  /follow                 Bei Live-Gang eines Streamers gepingt werden
 27322  /help                   Alle Bot-Befehle anzeigen
 26836  /kick                   Mitglied kicken
 27065  /leaderboard            Top-10 der Community nach XP
 27278  /livenow                Welche getrackten User sind gerade live
 27308  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 27139  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 26871  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 27051  /rank                   Dein Level und Rang anzeigen
 27265  /recstatus              Aktuell laufende Aufnahmen
 26812  /remove_role            Rolle/Gruppe entfernen
 26724  /restream_status        Restream-Status
 26823  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 27016  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 27034  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 27364  /stats                  Statistik zu einem getrackten Streamer
 26636  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 27660  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 27557  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 27533  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 26858  /timeout                Mitglied stummschalten (Minuten)
 27436  /topstreamers           Rangliste der Streamer nach Aufnahmen
 26666  /track                  TikTok-User tracken
 26650  /tracklist              Getrackte TikTok-User dieses Servers
 27353  /unfollow               Live-Pings für einen Streamer abbestellen
 26699  /untrack                TikTok-User nicht mehr tracken
 27386  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 27410  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 28144  on_member_join
 28106  on_message
 27747  on_raw_reaction_add
 28179  on_ready
```

## Top-Level-Symbole in bot_v37.py (555 Funktionen, 2 Klassen)

```
  2465-2466   _abo_key
  2486-2504   _abo_probe_dump
 25547-25557  _active_recorder_sync
 20189-20196  _ad_allowlist
 21311-21317  _agent_for
 25559-25577  _ai_calls_total_sync
 21320-21336  _ai_telemetry
 21818-21836  _alert
 28292-28342  _alert_monitor_loop
 28716-28778  _announce_loop
  3407-3410   _anthropic_key
  3417-3419   _anthropic_model
 10337-10340  _arg_int
  2457-2462   _as_dict
 18049-18054  _audio_cfg
 21972-21994  _audio_tap_cmd
 10501-10512  _auth_cookie
 10468-10497  _auth_guard
  1613-1618   _auto_on
 22868-22886  _auto_restream_loop
 29846-29861  _azrael_broadcast_reply
 29746-29768  _azrael_chat_reply
 29729-29743  _azrael_chat_should_reply
 13083-13101  _azrael_creator_take
 29774-29776  _azrael_gate_cfg
 21341-21355  _azrael_live_state
 24598-24612  _azrael_overlay_state
 21701-21755  _azrael_proactive_loop
 21160-21216  _azrael_reaction_to_chats
 29779-29786  _azrael_reply_all_chats
 29716-29726  _azrael_self_names
 29814-29843  _azrael_send_to
 21358-21379  _azrael_system
 28456-28459  _backup_active
 28537-28550  _backup_loop
 20077-20078  _badwords_path
 28257-28266  _brain_growth_loop
 11378-11405  _brain_growth_snapshot
  2393-2413   _brain_hint_delay
 11370-11372  _brain_history_for
  6829-6857   _brain_notify
 11347-11368  _brain_record
 11374-11376  _brain_stream_recent
 14560-14577  _browser_push
  6873-6960   _build_daily_summary
  2896-3076   _build_native_cmd
 18397-18584  _build_restream_cmd
  3120-3153   _build_ytdlp_cmd
 25499-25506  _cached_probe
  5651-5678   _can_stop_tracking
  1793-1815   _capture_set_cookies
 15737-15740  _cfg_get
 15743-15745  _cfg_set
 24342-24377  _channel_set_all
 17647-17650  _chat_connected
 17653-17669  _chat_disconnected
  8902-8913   _chat_is_forum
 17689-17691  _chat_sanitize
 17693-17702  _chat_src_ok
 17632-17644  _chat_stat
 17672-17675  _chat_stats_snapshot
  3682-3693   _check_ai_alive_sync
  3696-3708   _check_ai_models_sync
 25508-25521  _check_redis_alive_sync
 25523-25543  _check_redis_version_sync
 11977-12020  _classify_pool_anonymity
 12023-12040  _classify_pool_anonymity_bg
   775-779    _claude_chat_sync_metered
 10362-10369  _client_ip
 28810-28837  _clip_prune
 28840-28850  _clip_recfile_for
 29366-29372  _clip_should_velocity
 28891-28973  _clip_to_discord
  3580-3589   _close_ai_session
 29890-29905  _cohost_broadcast
 29872-29876  _cohost_cfg
 29931-29943  _cohost_fire_highlight
 29879-29887  _cohost_gate
 29908-29928  _cohost_highlight
 29022-29056  _community_events_loop
 11201-11203  _conv_messages
  7253-7293   _cookie_alarm_loop
  1865-1869   _cookie_autorefresh_info
  1770-1774   _cookie_header
 14610-14642  _cpu_load_snapshot
  3890-3902   _create_index_safe
 13051-13066  _creator_activity
 13107-13130  _creator_dossier_generate
 13069-13080  _creator_facts_line
 25760-25866  _crowdsec_status
 25726-25757  _crowdsec_via_lapi
 25591-25609  _cscli_bin
 25615-25628  _cscli_path
  7146-7171   _daily_summary_loop
 25646-25663  _darf_journal_lesen
 28269-28289  _db_maintenance_loop
  7118-7143   _db_vacuum_loop
 20212-20236  _detect_foreign_ad
  1352-1363   _diag_path_owner
 21607-21651  _director_finalize
 22418-22425  _director_for
 21556-21604  _director_mark
 29260-29295  _disc_automod_check
 29233-29239  _disc_state_get
 29242-29249  _disc_state_set
 26309-26322  _discord_guild_filesize_bytes
 26508-26517  _discord_invite
 29194-29230  _discord_live_thread
 21758-21770  _discord_notify
 26409-26434  _discord_ops_alert
 29092-29190  _discord_post_user
 26573-28254  _discord_run_once
 26447-26505  _discord_start
 28781-28787  _discord_stop
 26330-26332  _discord_upload_limit_label
 26325-26327  _discord_upload_limit_mb
  7174-7248   _disk_alarm_loop
 31272-31321  _disk_autoclean
 31324-31337  _disk_guard_loop
 31264-31269  _disk_pct
 24655-24658  _donations_unknown_count
 18006-18008  _drawtext_chain
 15189-15191  _dump_all_threads
 11902-11966  _enrich_proxies_with_geo
  2010-2054   _ensure_cookie_file_netscape
 26520-26570  _ensure_discord_invite
 28987-29019  _ensure_error_channel
 12145-12182  _ensure_proxy_ready
  8915-8938   _ensure_topic
   638-640    _env_int
   643-645    _env_int_range
 29059-29089  _error_channel_loop
 21802-21815  _event_webhook
 16940-16946  _evo_build_dir
 16949-16956  _evo_version
 17232-17313  _evolution_cycle
 16965-16985  _evolution_llm_note
 17316-17326  _evolution_loop
 16988-17229  _evolution_write_build
  6271-6305   _extract_file_payload
  2142-2144   _extract_urls_from_streamurl_node
 25631-25638  _f2b_sudo_hint
 21838-21840  _faster_whisper_available
 20101-20113  _fetch_ldnoobw_de
 11791-11809  _fetch_proxy_list
 22252-22280  _fetch_tiktok_room_id
   709-712    _ff_cmd
 15860-15873  _ffmpeg_version_str
 18169-18174  _find_chromium
  3113-3117   _find_external_recorder
  2147-2149   _find_stream_urls
 15788-15813  _fire_webhooks
  8029-8038   _fork_safe
   790-799    _freeai_chat_sync_metered
 25681-25723  _geo_lookup_ips
  3569-3578   _get_ai_session
  7863-7903   _get_live_info
  2683-2690   _get_resolve_semaphore
  8264-8629   _handle_single_tracking
 31116-31118  _hb
 31121-31138  _hb_while
 17707-17709  _highlight_cfg
 17712-17741  _highlight_observe
 18177-18182  _htmlov_screenshot_cmd
 21996-22006  _httpx_proxy
 15821-15833  _in_quiet_hours
 32105-32136  _install_fast_eventloop
 10232-10286  _install_fast_json
 15194-15210  _install_faulthandler
 23111-23120  _intel_ensure_schema
 23158-23189  _intel_index_loop
 23132-23142  _intel_index_one
 23123-23129  _intel_semantic
  5640-5649   _is_authorized
  8194-8200   _is_dead
  2132-2134   _is_hevc
 25666-25672  _is_private_ip
  1516-1523   _is_process_running
  6859-6870   _is_quiet_hours
  1160-1169   _is_upload_window
 10321-10334  _json_error_handler
  7076-7106   _kick_broadcaster_id
 12557-12576  _kick_channel_live
  6993-7035   _kick_follower_count
 13568-13581  _kick_oauth_exchange
 13584-13586  _kick_oauth_page
 13527-13531  _kick_redirect_public
 13518-13524  _kick_redirect_source
 13504-13515  _kick_redirect_uri
  6978-6980   _kick_slug
 13534-13565  _kick_user_token
  3939-3942   _kind_from_filename
 15850-15855  _latest_popularity
 20123-20129  _learned_load
 20120-20121  _learned_path
 20131-20139  _learned_save
 22633-22663  _live_react_loop
 22429-22622  _live_react_worker
 21219-21230  _live_transcript_push
 22624-22631  _live_users
 21654-21698  _living_title_loop
 20080-20088  _load_banned_words_file
  1691-1764   _load_cookies_dict
 28462-28534  _local_backup_scan
 10303-10317  _log_5xx
 18592-18604  _looks_like_codec_err
 18587-18589  _looks_like_source_expired
  8110-8140   _loop_fehler
 15214-15223  _loop_heartbeat
 31086-31113  _loop_lag_monitor
 15333-15336  _loop_not_ready
 15226-15294  _loop_watchdog_thread
 21099-21113  _loyalty_add
 21090-21096  _loyalty_get
 21116-21124  _loyalty_top
 16234-16252  _manual_donations_rows
 16255-16257  _manual_donations_total
  8202-8203   _mark_dead
 12724-12753  _marketing_cfg
 12715-12721  _marketing_default_targets
 12710-12712  _marketing_enabled
 12767-12782  _marketing_flavor
 12837-12853  _marketing_loop
 12785-12795  _marketing_post_discord
 12798-12810  _marketing_post_telegram
 12813-12834  _marketing_publish
 12756-12760  _marketing_state_obj
 12763-12764  _marketing_state_save
 29793-29811  _maybe_handle_command
 31423-31447  _maybe_hype_clip
  3857-3880   _migrate_columns
 30070-30081  _mod_is_exempt
 30084-30089  _mod_warn_first
 30092-30095  _mod_warn_text
 17495-17503  _modlog
   913-915    _multistream_targets
  8041-8042   _nc_create_subprocess_exec
  8045-8046   _nc_create_subprocess_shell
 12948-12964  _news_cfg
 12935-12937  _news_enabled
 13002-13043  _news_facts
 13157-13179  _news_generate
 13362-13379  _news_loop
 12940-12945  _news_output_path
 13046-13048  _news_phrase
 13133-13154  _news_phrase_impl
 12977-12984  _news_read
 12967-12970  _news_state_obj
 12973-12974  _news_state_save
 12987-12999  _news_write
 17533-17535  _normalize_ingest
  2324-2341   _note_check_duration
 21245-21253  _oracle_memories
 21511-21545  _oracle_memorize
 21256-21269  _oracle_persona
 21238-21242  _oracle_recent_text
 17832-17840  _ov_atomic_write
 17820-17826  _ov_bar
 20036-20048  _ov_clip_text
 17829-17830  _ov_oneline
 24666-24695  _overlay_push
 18123-18166  _overlay_render_size
 17594-17598  _overlay_session_reset
 24614-24617  _overlay_src_ok
 20199-20209  _own_invites
 16215-16231  _parse_eur
 18118-18120  _parse_size
 25874-25954  _parse_ssh_attacks
  7465-7498   _pause_resume_cmd
  1819-1863   _persist_refreshed_cookies
  1657-1689   _pick_checked_pull_proxy
 10398-10411  _pin_auth_value
 10457-10458  _pin_clear_fail
 10437-10440  _pin_locked
 10443-10454  _pin_note_fail
 10414-10434  _pin_ok
 24504-24506  _piper_available
 24469-24491  _piper_list_voices
 24511-24536  _piper_pick_model
 24548-24595  _piper_say
 24462-24466  _piper_voice_roots
 15750-15785  _post_json_threaded
 18097-18115  _probe_video_size
  1544-1561   _proc_is_recorder
 11889-11900  _proxy_geo_cache_put
 12116-12142  _proxy_pool_refresh_loop
  1623-1654   _proxy_report_recording
 15179-15181  _prune_stall_dumps
 13182-13303  _public_stats
 21773-21799  _push_notify
 10559-10561  _pwa_dir
 11860-11875  _quick_validate_proxy
 15816-15818  _quiet_hours_config
 10524-10557  _rate_guard
 21064-21070  _react_warn
  7949-7988   _reap_proc
  2364-2386   _record_check_outcome
   704-706    _redact_stream_urls
 12043-12113  _refresh_proxy_pool
 24494-24500  _resolve_piper_model
  2158-2248   _resolve_via_html
  2506-2660   _resolve_via_webcast_api_v2
  2723-2785   _resolve_via_ytdlp
 29412-29541  _resolve_youtube_ingest
 22702-22709  _restream_active_platforms
 17579-17590  _restream_active_sources
 22283-22382  _restream_chat_guardian
 17744-17816  _restream_chat_push
 17506-17518  _restream_enabled
 18185-18272  _restream_html_overlay_start
 18275-18288  _restream_html_overlay_stop
  1108-1110   _restream_layout_mode
 17544-17567  _restream_overlay_files
 22667-22699  _restream_platform_state
 22830-22865  _restream_resume_after_restart
 18336-18394  _restream_tts_enqueue_wav
 18059-18091  _restream_tts_feeder
 18056-18057  _restream_tts_fifo_path
 18291-18318  _restream_tts_start
 18320-18334  _restream_tts_stop
 22712-22827  _restream_verify_loop
 28427-28439  _retention_loop
 28386-28424  _retention_scan
  2468-2470   _room_is_abo
  6309-6426   _run_ai_call
 15317-15330  _run_async_from_flask
 25675-25678  _run_priv
 32093-32101  _run_selfcheck_and_exit
 28442-28453  _s3_client
  8205-8251   _safe_send
  4792-4808   _sample_net_throughput
 20090-20098  _save_banned_words_file
  2416-2443   _schedule_next_check
 28345-28383  _scheduler_loop
  3883-3887   _schema_pk
 15338-15343  _scraper_session
 30098-30137  _screen_full
 13894-13931  _sec_headers
  2137-2139   _select_stream_from_data_section
 31906-32090  _selfcheck
  1183-1187   _should_defer_upload
 28853-28888  _shrink_for_discord
 10564-10576  _sicheres_ziel
 31344-31361  _sign_health_check
 31364-31383  _sign_health_loop
  8058-8069   _spawn
  8072-8102   _spawn_from_flask
 25998-26001  _st_befund
 22008-22249  _start_chat_listener
 15297-15314  _start_loop_watchdog
 13327-13353  _stats_loop
 13306-13309  _stats_output_path
 13312-13324  _stats_write
  8697-8711   _storage_cleanup_loop
 31403-31410  _story_for
  3175-3181   _stream_url_expiry
  3190-3196   _stream_url_is_fresh
  3183-3188   _stream_url_ttl
 20163-20170  _streamer_persona_get
 20145-20151  _streamer_personas_load
 20142-20143  _streamer_personas_path
 20153-20161  _streamer_personas_save
 18011-18015  _studio_chain
 28559-28681  _system_backup
 28684-28712  _system_backup_loop
 11812-11851  _test_proxy
 12598-12607  _testpush_cfg
 12610-12627  _testpush_exec
 12579-12595  _testpush_resolve_live
  8874-8884   _tg_topics_load_into_mem
  8871-8872   _tg_topics_path
  8886-8893   _tg_topics_save
 25208-25256  _tiktok_account_exists
 10372-10380  _token_ok
  8896-8900   _topic_forget
 15836-15847  _tracking_max_duration
  1410-1433   _try_attach_file_handler
 24538-24546  _tts_cleanup
 12483-12486  _tunnel_effective
 23964-24017  _twitch_channel_status
 30140-30283  _twitch_chat_loop
 29954-30057  _twitch_eventsub_loop
 16660-16663  _twitch_oauth_page
  1206-1219   _upload_queue_add
  1230-1232   _upload_queue_count
  1189-1198   _upload_queue_load
  1179-1181   _upload_queue_path
  1221-1228   _upload_queue_remove
  1200-1204   _upload_queue_save
  1234-1272   _upload_window_loop
  7922-7929   _uptime_s
 17521-17530  _url_host
   684-701    _url_ohne_zugang
   768-772    _usage_record_claude
  8143-8187   _verbindung_verloren
  7038-7066   _viewer_sample_loop
  7108-7115   _viewer_stats
 10461-10464  _wants_html
  7932-7946   _warn_empty_env
 31159-31254  _watchdog_loop
 29695-29703  _wchat_thank_ok
 21842-21872  _whisper_get_model
  8019-8026   _whisper_native_section
 21051-21057  _whisper_pool
 21941-21970  _whisper_segments
 21874-21938  _whisper_transcribe
 17842-18004  _write_restream_overlay
 30311-30384  _youtube_api_chat_loop
 24020-24123  _youtube_api_status
 24126-24193  _youtube_channel_status
 30387-30544  _youtube_chat_loop
 29547-29560  _youtube_restream_autoconfig
 29563-29587  _youtube_restream_autoconfig_inner
 29653-29681  _youtube_send
 24298-24339  _youtube_set_channel
 29590-29624  _yt_access_token
 29627-29642  _yt_live_chat_id
 30304-30308  _yt_oauth_configured
 29648-29650  _yt_sendrate_cfg
 30286-30301  _yt_timeout
  2707-2708   _ytdlp_detect_available
  2710-2721   _ytdlp_note_result
 15184-15186  _zombie_child_count
  7799-7823   about
  4058-4062   add_ai_log_entry
  3975-3978   add_archive_entry
  4905-4920   add_archive_rule
  4487-4521   add_recording
  4148-4165   add_tracking
  4582-4599   add_tracking_tag
  6429-6462   ai
  3722-3761   ai_chat
  3795-3805   ai_history_append
  3807-3812   ai_history_clear
  3784-3793   ai_history_load
  3769-3782   ai_rate_limit_check
  6491-6499   aireset
 21382-21401  azrael_chat
 30549-30671  brain_cmd
  3199-3383   build_recording_cmd
  4168-4245   bulk_add_trackings
  7296-7355   bulkadd
  8714-8854   check_all_trackings
  4332-4344   claim_live_transition
 20239-20994  class KickModerator
 18607-19923  class RestreamManager
 12227-12269  classify_proxy_anonymity
  6537-6735   cleanup
  5500-5541   cleanup_old_recordings
  4478-4485   clear_recording
 29298-29363  clip_moment
  5053-5096   cluster_failures
  4736-4785   compute_storage_forecast
  7418-7462   cookies_cmd
  5342-5348   cookies_days_old
  4139-4145   count_trackings_for_chat
  4045-4056   decide_preferred_recorder
  3985-3988   delete_archive_entry
  4922-4930   delete_archive_rule
  5966-6113   diag
 30783-30844  einnahmen_cmd
  4730-4733   find_recordings_by_fingerprint
  4006-4022   finish_recording_attempt
  4277-4287   get_all_active_trackings
  4084-4087   get_all_checks
  4523-4526   get_all_recordings
  4624-4634   get_all_tags_with_counts
  4707-4710   get_annotations_for_recording
  3980-3983   get_archive_entry
  4700-4703   get_bookmarked_recordings
  1886-2003   get_cookie_health
  4573-4579   get_event_log
  4029-4043   get_last_recording_attempt
  2788-2893   get_live_status
  5256-5259   get_manual_recordings
  4715-4718   get_or_compute_inspect_sync
  5576-5620   get_outcome_breakdown
  4681-4689   get_priority_poll_interval
  4883-4892   get_profile_snapshots
  4064-4074   get_recent_ai_log
  4024-4027   get_recent_recording_attempts
  4528-4531   get_recording_by_id
  4693-4696   get_recording_note
  3517-3540   get_redis
  4115-4131   get_stats
  5467-5498   get_storage_stats
  4614-4622   get_tags_for_tracking
  5023-5037   get_tiktok_status_distribution
  4668-4679   get_tracking_priority
  4346-4355   get_tracking_state
  4273-4275   get_trackings_for_group
  5272-5275   get_trash_recordings
  9558-10200  handle_recording_finished
  3905-3930   init_db
  5390-5444   inspect_stream_url
 24661-24663  is_revenue_platform
  4895-4903   list_archive_rules
  5770-5808   live
  8254-8262   live_check_worker
  3592-3626   llm_chat
  3649-3677   llm_chat_sync
  3634-3646   llm_list_models
  4539-4565   log_event
  1478-1511   log_recording_failure
  7612-7661   logs_cmd
 31451-31896  main
  6465-6488   on_ai_media
  7738-7764   on_ai_reply
  7767-7796   on_azrael_mention
  7828-7858   on_callback
 21404-21508  oracle_handle
  7501-7504   pause_tracking
  5630-5635   profile_keyboard
  5351-5387   quick_restart_tracking
  7563-7609   quota
  8631-8694   reaper_loop
  5019-5021   record_tiktok_status
  6504-6534   recstatus
  3542-3550   redis_get_json
  3552-3558   redis_set_json
  4247-4271   remove_tracking
  4601-4612   remove_tracking_tag
 30847-30857  report_cmd
 12272-12274  report_proxy_result
  2251-2278   resolve_tiktok_live_stream
  5267-5270   restore_recording
  7507-7510   resume_tracking
  4933-5013   run_archive_rules
 30860-31066  run_bot
 15106-15153  run_flask
  4811-4856   sample_bandwidth_for_active
  4862-4881   save_profile_snapshot
  4076-4082   save_tiktok_check
  4470-4476   set_recording_file
  4290-4328   set_tracking_paused
  4637-4666   set_tracking_priority
  5262-5265   soft_delete_recording
  8943-9556   split_and_send_video
  5683-5725   start
  3990-4004   start_recording_attempt
  6738-6776   stats
  5237-5254   stop_manual_recording
  7513-7560   stoprec
  6963-6971   summary_cmd
  7664-7735   sysres
  6115-6259   teststream
  5727-5768   tiktok
  7358-7415   topusers
  5845-5902   track
  5810-5842   track_exact
  5916-5964   tracklist
  5103-5235   trigger_manual_recording
  4431-4468   try_acquire_recording_lock
  5278-5337   universal_search
  5904-5914   untrack
 30674-30780  update_cmd
  4725-4728   update_recording_fingerprint
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
