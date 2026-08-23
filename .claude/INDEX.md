# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot_v37.py (279)

```
 10539  GET              /                                                dashboard
 16071  GET              /api/abo/status                                  api_abo_status
 10638  GET              /api/active-recordings                           api_active_recordings
 16146  GET              /api/activity-pulse                              api_activity_pulse
 15499  GET              /api/ai-log                                      api_ai_log
 11036  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail
 25210  GET              /api/ai/anomalies                                api_ai_anomalies
 12653  POST             /api/ai/ask                                      api_ai_ask
 13891  POST             /api/ai/claude/save                              api_claude_save
 13871  GET              /api/ai/claude/status                            api_claude_status
 13909  POST             /api/ai/claude/test                              api_claude_test
 12919  GET              /api/ai/config                                   api_ai_config
 11208  GET              /api/ai/conversations                            api_ai_conversations_list
 11219  POST             /api/ai/conversations                            api_ai_conversations_create
 11229  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get
 11252  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete
 11259  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch
 11270  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send
 11403  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream
 11994  POST             /api/ai/diagnose                                 api_ai_diagnose
 25448  GET              /api/ai/forecast-storage                         api_ai_forecast_storage
 25482  GET              /api/ai/health-score/<username>                  api_ai_health_score
 11192  GET              /api/ai/models                                   api_ai_models
 25163  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive
 25143  POST             /api/ai/query                                    api_ai_query
 25316  GET              /api/ai/recommendations                          api_ai_recommendations
 25364  GET              /api/ai/report                                   api_ai_report
 25415  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice
 25274  GET              /api/ai/segments                                 api_ai_segments
 25118  GET              /api/ai/skills                                   api_ai_skills
 15906  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 23536  GET/POST         /api/audio/config                                api_audio_config
 23566  POST             /api/audio/testtone                              api_audio_testtone
 16012  GET/POST         /api/auto-archive-rules                          api_archive_rules
 16036  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 16040  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12869  GET              /api/automation/status                           api_automation_status
 12891  POST             /api/automation/toggle                           api_automation_toggle
 14704  GET              /api/azrael/agents                               api_azrael_agents
 12772  POST             /api/azrael/ask                                  api_azrael_ask
 23772  GET/POST         /api/azrael/context                              api_azrael_context
 14331  GET              /api/azrael/core                                 api_azrael_core
 23906  POST             /api/azrael/live_pause                           api_azrael_live_pause
 23896  GET              /api/azrael/live_status                          api_azrael_live_status
 23914  POST             /api/azrael/live_test                            api_azrael_live_test
 14713  GET              /api/azrael/memories                             api_azrael_memories
 23962  POST             /api/azrael/persona                              api_azrael_persona_set
 23953  GET              /api/azrael/personas                             api_azrael_personas
 23990  GET              /api/azrael/piper_status                         api_azrael_piper_status
 23745  POST             /api/azrael/react                                api_azrael_react
 23781  GET              /api/azrael/reaction                             api_azrael_reaction
 23933  GET              /api/azrael/reactions                            api_azrael_reactions
 23983  GET              /api/azrael/transcript                           api_azrael_transcript
 23868  POST             /api/azrael/tts_test                             api_azrael_tts_test
 23843  GET              /api/azrael/voices                               api_azrael_voices
 24007  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 11512  GET              /api/backoff-watch                               api_backoff_watch
 15270  POST             /api/backup/run                                  api_backup_run
 15236  GET              /api/backup/status                               api_backup_status
 15225  POST             /api/backup/system                               api_backup_system
 15978  GET              /api/bandwidth/live                              api_bandwidth_live
 15891  GET              /api/bookmarks                                   api_bookmarks_list
 11775  GET              /api/brain                                       api_brain
 11712  GET              /api/brain/alarms                                api_brain_alarms
 11697  GET              /api/brain/creator                               api_brain_creator
 11674  GET              /api/brain/graph                                 api_brain_graph
 11735  GET              /api/brain/growth                                api_brain_growth
 10135  GET              /api/brain/health                                api_brain_health
 24488  GET              /api/channel/categories                          api_channel_categories
 24494  POST             /api/channel/set                                 api_channel_set
 24304  GET              /api/channels/status                             api_channels_status
 23091  POST             /api/chat/send                                   api_chat_send
 14971  GET              /api/chat/send_status                            api_chat_send_status
 10619  GET              /api/checks                                      api_checks
 23809  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 23792  GET              /api/clips                                       api_clips
 23825  POST/DELETE      /api/clips/clear                                 api_clips_clear
 23411  GET              /api/cohost                                      api_cohost
 23423  POST             /api/cohost/config                               api_cohost_config
 16710  GET              /api/community/stats                             api_community_stats
 25820  POST             /api/config/restore                              api_config_restore
 25805  GET              /api/config/snapshot                             api_config_snapshot
 16169  GET              /api/cookies/age                                 api_cookies_age
 10686  GET              /api/cookies/health                              api_cookies_health
 10693  POST             /api/cookies/update                              api_cookies_update
 25771  GET              /api/data/export                                 api_data_export
 17220  GET              /api/db/export                                   api_db_export
 17247  POST             /api/db/import                                   api_db_import
 17207  GET              /api/db/summary                                  api_db_summary
 23337  GET              /api/debug/threads                               api_debug_threads
 26706  GET              /api/defense/attacks                             api_defense_attacks
 26673  GET              /api/defense/crowdsec                            api_defense_crowdsec
 26691  GET              /api/defense/fail2ban                            api_defense_fail2ban
 26397  GET              /api/defense/overview                            api_defense_overview
 15332  POST             /api/discord/announce                            api_discord_announce
 15060  GET              /api/discord/clips_week                          api_discord_clips_week
 15276  GET              /api/discord/community                           api_discord_community
 14999  GET              /api/discord/invite                              api_discord_invite
 14462  GET              /api/discord/overview                            api_discord_overview
 14548  POST             /api/discord/webhook_test                        api_discord_webhook_test
 16787  POST             /api/donations/add                               api_donations_add
 16820  GET              /api/donations/manual                            api_donations_manual
 16828  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete
 16723  POST             /api/donations/reset                             api_donations_reset
 16844  GET              /api/donations/summary                           api_donations_summary
 15960  GET              /api/events                                      api_events
 15107  GET              /api/events/stream                               api_events_stream
 17875  GET              /api/evolution/changelog                         api_evolution_changelog
 17860  GET              /api/evolution/history                           api_evolution_history
 17800  GET              /api/evolution/learned                           api_evolution_learned
 17822  GET              /api/evolution/proposals                         api_evolution_proposals
 17843  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 17790  POST             /api/evolution/run                               api_evolution_run
 17890  GET              /api/evolution/snapshots                         api_evolution_snapshots
 17755  GET              /api/evolution/status                            api_evolution_status
 17054  GET              /api/finanzamt/entries                           api_finanzamt_entries
 17074  POST             /api/finanzamt/entry                             api_finanzamt_add
 17101  GET              /api/finanzamt/export.csv                        api_finanzamt_csv
 15973  GET              /api/forecast/storage                            api_forecast_storage
 12907  GET              /api/freeai/status                               api_freeai_status
 14404  GET              /api/health                                      api_health
 15991  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 15987  GET              /api/heatmap/recordings                          api_heatmap_recordings
 23460  GET              /api/highlights                                  api_highlights
 23472  POST             /api/highlights/config                           api_highlights_config
 24345  GET              /api/kick/channel                                api_kick_channel
 24366  POST             /api/kick/channel                                api_kick_channel_set
 14131  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 14199  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 14177  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 14116  GET              /api/kick/oauth/start                            api_kick_oauth_start
 14156  GET              /api/kick/oauth/status                           api_kick_oauth_status
 23584  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 23653  POST             /api/kickmod/config                              api_kickmod_config
 23698  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 23712  GET              /api/kickmod/learned                             api_kickmod_learned
 23739  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 23719  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 24050  POST             /api/kickmod/say                                 api_kickmod_say
 24026  POST             /api/kickmod/start                               api_kickmod_start
 23624  GET              /api/kickmod/status                              api_kickmod_status
 24037  POST             /api/kickmod/stop                                api_kickmod_stop
 10471  POST             /api/login                                       dashboard_login_submit
 16695  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 13358  POST             /api/marketing/config                            api_marketing_config
 13383  GET              /api/marketing/preview                           api_marketing_preview
 13393  POST             /api/marketing/send-now                          api_marketing_send_now
 13332  GET              /api/marketing/status                            api_marketing_status
 13350  POST             /api/marketing/toggle                            api_marketing_toggle
 23487  GET              /api/moderation/feed                             api_moderation_feed
 13962  POST             /api/news/config                                 api_news_config
 13928  GET              /api/news/creators                               api_news_creators
 13939  POST             /api/news/creators/generate                      api_news_creators_generate
 14004  POST             /api/news/generate-now                           api_news_generate_now
 13999  GET              /api/news/items                                  api_news_items
 13990  GET              /api/news/preview                                api_news_preview
 13858  GET              /api/news/status                                 api_news_status
 13954  POST             /api/news/toggle                                 api_news_toggle
 16552  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 14936  GET              /api/notify/status                               api_notify_status
 14947  POST             /api/notify/test                                 api_notify_test
 14922  GET              /api/ops/audit                                   api_ops_audit
 16623  GET              /api/ops/db-stats                                api_ops_db_stats
 16651  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown
 14728  GET              /api/ops/errors                                  api_ops_errors
 16572  GET              /api/ops/healthcheck                             api_ops_healthcheck
 17302  GET              /api/ops/log-tail                                api_ops_log_tail
 12752  GET              /api/ops/logtail                                 api_ops_logtail
 14669  GET              /api/ops/metrics                                 api_ops_metrics
 14652  GET              /api/ops/resource_history                        api_ops_resource_history
 17276  GET              /api/ops/version                                 api_ops_version
 10889  GET              /api/outcomes                                    api_outcomes
 24969  POST             /api/overlay/config                              api_overlay_config
 24956  POST             /api/overlay/event                               api_overlay_event
 24861  GET              /api/overlay/state                               api_overlay_state
 10922  GET              /api/profile/<username>                          api_profile
 16177  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 15999  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 16125  GET              /api/proxy/heatmap                               api_proxy_heatmap
 16102  GET              /api/proxy/trend                                 api_proxy_trend
 13832  GET              /api/public/stats                                api_public_stats
 10573  GET              /api/pulse                                       api_pulse
 15523  GET              /api/recording-attempts                          api_recording_attempts
 23026  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 23004  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 23045  POST             /api/restream/<int:rid>/start                    api_restream_start
 23358  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 24823  GET              /api/restream/chatfeed                           api_restream_chatfeed
 22980  POST             /api/restream/create                             api_restream_create
 14207  GET              /api/restream/deck                               api_restream_deck
 12843  GET              /api/restream/health                             api_restream_health
 24845  POST             /api/restream/layout                             api_restream_layout
 22953  GET              /api/restream/list                               api_restream_list
 12816  POST             /api/restream/report                             api_restream_report
 23371  POST             /api/restream/start_all                          api_restream_start_all
 23397  POST             /api/restream/stop_all                           api_restream_stop_all
 13106  GET              /api/restream/testpush                           api_testpush_status
 13131  POST             /api/restream/testpush                           api_testpush_run
 16960  GET              /api/restream/verify                             api_restream_verify
 15038  GET              /api/retention/preview                           api_retention_preview
 15047  POST             /api/retention/run                               api_retention_run
 25886  POST             /api/schedule/add                                api_schedule_add
 25876  GET              /api/schedule/list                               api_schedule_list
 25911  POST             /api/schedule/remove                             api_schedule_remove
 15876  GET              /api/search                                      api_search
 26444  GET              /api/selftest                                    api_selftest
 23062  GET              /api/shield/stats                                api_shield_stats
 10592  GET              /api/stats                                       api_stats
 16140  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern
 16067  GET              /api/stats/tiktok-status                         api_tiktok_status
 25851  GET              /api/stats/timeline                              api_stats_timeline
 10660  GET              /api/storage                                     api_storage
 10667  POST             /api/storage/cleanup                             api_storage_cleanup
 16053  GET              /api/stream/inspect/<username>                   api_stream_inspect
 12793  GET              /api/stream/timeline                             api_stream_timeline
 14536  GET              /api/stream/transcript                           api_stream_transcript
 25519  GET              /api/streamer/compare                            api_streamer_compare
 25718  POST             /api/streamer/delete/<username>                  api_streamer_delete
 15012  GET              /api/streamer/detail                             api_streamer_detail
 25743  GET              /api/streamer/digest/<username>                  api_streamer_digest
 25623  GET              /api/streamer/dormant                            api_streamer_dormant
 25699  GET              /api/streamer/exists/<username>                  api_streamer_exists
 25578  GET              /api/streamer/journal/<username>                 api_streamer_journal
 25543  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 25603  GET              /api/streamer/watchlist                          api_streamer_watchlist
 14371  GET              /api/streamers/wall                              api_streamers_wall
 10809  GET              /api/summary/preview                             api_summary_preview
 15588  GET              /api/system                                      api_system
 16908  GET              /api/system/check_timing                         api_check_timing
 17188  GET              /api/system/config_drift                         api_config_drift
 14572  GET              /api/system/config_snapshot                      api_system_config_snapshot
 14783  GET              /api/system/preflight                            api_system_preflight
 14909  GET              /api/system/preflight_history                    api_system_preflight_history
 15172  GET              /api/system/resilience                           api_system_resilience
 15911  GET              /api/tags                                        api_tags_list
 10633  GET              /api/top                                         api_top
 12726  GET              /api/trackings                                   api_trackings
 16441  POST             /api/trackings/<int:tid>/collection              api_tracking_collection
 16474  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration
 15947  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority
 16160  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart
 16503  GET              /api/trackings/<int:tid>/settings                api_tracking_settings
 15933  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags
 15362  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes
 15409  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause
 15438  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck
 15420  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume
 10826  POST             /api/trackings/bulk                              api_trackings_bulk
 15377  GET              /api/trackings/export                            api_trackings_export
 15915  GET              /api/trackings/tags-map                          api_trackings_tags_map
 16215  GET              /api/trackings/watchlist-export                  api_watchlist_export
 11567  GET              /api/trend-7d                                    api_trend_7d
 23857  GET              /api/tts/<fn>                                    api_tts_file
 12986  POST             /api/tunnel/set                                  api_tunnel_set
 12965  GET              /api/tunnel/status                               api_tunnel_status
 12997  POST             /api/tunnel/test                                 api_tunnel_test
 12978  POST             /api/tunnel/toggle                               api_tunnel_toggle
 17160  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 17137  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 17119  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 24997  GET              /api/upload_window                               api_upload_window
 10903  GET              /api/userstats                                   api_userstats
 14015  GET              /api/version                                     api_version
 17016  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 17037  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 17001  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 16985  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 30124  GET              /api/youtube/sendrate                            api_youtube_sendrate
 15561  GET              /archive/<int:eid>/download                      archive_download
 15618  GET              /download/<int:recording_id>                     download
 15484  GET              /health                                          health
 23306  GET              /healthz                                         healthz
 10460  GET              /login                                           dashboard_login_page
 10494  GET              /logout                                          dashboard_logout
 10501  GET              /manifest.webmanifest                            pwa_manifest
 14600  GET              /metrics                                         api_prometheus_metrics
 24806  GET              /overlay                                         overlay_page
 10525  GET              /pwa-icon-<variant>.png                          pwa_icon
 10511  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (66)

```
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
 27149  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 27608  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 27240  /assign_role            Rolle/Gruppe einem Mitglied geben
 27286  /ban                    Mitglied bannen
 27940  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 27864  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 27904  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 27889  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 27731  /clips                  Letzte Highlight-Clips eines Users
 27201  /create_category        Kategorie anlegen
 27170  /create_channel         Text-Channel anlegen (optional in Kategorie)
 27229  /create_group           Nutzergruppe (= Rolle) anlegen
 27212  /create_role            Rolle / Nutzergruppe anlegen
 27186  /create_voice           Voice-Channel anlegen
 27522  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 27638  /event                  Community-Event ankündigen (Admin) — mit Countdown
 27681  /events                 Kommende Community-Events anzeigen
 27777  /follow                 Bei Live-Gang eines Streamers gepingt werden
 27761  /help                   Alle Bot-Befehle anzeigen
 27275  /kick                   Mitglied kicken
 27504  /leaderboard            Top-10 der Community nach XP
 27717  /livenow                Welche getrackten User sind gerade live
 27747  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 27578  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 27310  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 27490  /rank                   Dein Level und Rang anzeigen
 27704  /recstatus              Aktuell laufende Aufnahmen
 27251  /remove_role            Rolle/Gruppe entfernen
 27163  /restream_status        Restream-Status
 27262  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 27455  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 27473  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 27803  /stats                  Statistik zu einem getrackten Streamer
 27075  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 28099  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 27996  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 27972  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 27297  /timeout                Mitglied stummschalten (Minuten)
 27875  /topstreamers           Rangliste der Streamer nach Aufnahmen
 27105  /track                  TikTok-User tracken
 27089  /tracklist              Getrackte TikTok-User dieses Servers
 27792  /unfollow               Live-Pings für einen Streamer abbestellen
 27138  /untrack                TikTok-User nicht mehr tracken
 27825  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 27849  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 28583  on_member_join
 28545  on_message
 28186  on_raw_reaction_add
 28618  on_ready
```

## Top-Level-Symbole in bot_v37.py (562 Funktionen, 2 Klassen)

```
  2373-2374   _abo_key
  2394-2412   _abo_probe_dump
 25986-25996  _active_recorder_sync
 20266-20273  _ad_allowlist
 21379-21385  _agent_for
 25998-26016  _ai_calls_total_sync
 12639-12649  _ai_dashboard_rate_check
 21388-21404  _ai_telemetry
 21886-21904  _alert
 28731-28781  _alert_monitor_loop
 29155-29217  _announce_loop
  3315-3318   _anthropic_key
  3328-3330   _anthropic_model
  3321-3323   _anthropic_model_raw
 10263-10266  _arg_int
  2365-2370   _as_dict
 18472-18477  _audio_cfg
 22040-22062  _audio_tap_cmd
 10396-10407  _auth_cookie
 10363-10392  _auth_guard
  1521-1526   _auto_on
 22929-22947  _auto_restream_loop
 30285-30300  _azrael_broadcast_reply
 30185-30207  _azrael_chat_reply
 30168-30182  _azrael_chat_should_reply
 13558-13576  _azrael_creator_take
 30213-30215  _azrael_gate_cfg
 21409-21423  _azrael_live_state
 24705-24719  _azrael_overlay_state
 21769-21823  _azrael_proactive_loop
 21228-21284  _azrael_reaction_to_chats
 30218-30225  _azrael_reply_all_chats
 30155-30165  _azrael_self_names
 30253-30282  _azrael_send_to
 21426-21447  _azrael_system
 28895-28898  _backup_active
 28976-28989  _backup_loop
 20154-20155  _badwords_path
 28696-28705  _brain_growth_loop
 11643-11670  _brain_growth_snapshot
  2301-2321   _brain_hint_delay
 11635-11637  _brain_history_for
  6834-6862   _brain_notify
 11612-11633  _brain_record
 11639-11641  _brain_stream_recent
 15086-15103  _browser_push
 11163-11183  _build_context_for_llm
  6878-6965   _build_daily_summary
  2804-2984   _build_native_cmd
 18820-19007  _build_restream_cmd
  3028-3061   _build_ytdlp_cmd
 25938-25945  _cached_probe
  5656-5683   _can_stop_tracking
  1701-1723   _capture_set_cookies
 16263-16266  _cfg_get
 16269-16271  _cfg_set
 24449-24484  _channel_set_all
 18070-18073  _chat_connected
 18076-18092  _chat_disconnected
  8860-8871   _chat_is_forum
 18112-18114  _chat_sanitize
 18116-18125  _chat_src_ok
 18055-18067  _chat_stat
 18095-18098  _chat_stats_snapshot
  3672-3683   _check_ai_alive_sync
  3686-3698   _check_ai_models_sync
 25947-25960  _check_redis_alive_sync
 25962-25982  _check_redis_version_sync
 12334-12377  _classify_pool_anonymity
 12380-12397  _classify_pool_anonymity_bg
   754-758    _claude_chat_sync_metered
 10288-10295  _client_ip
 29249-29276  _clip_prune
 29279-29289  _clip_recfile_for
 29805-29811  _clip_should_velocity
 29330-29412  _clip_to_discord
  3491-3500   _close_ai_session
 30329-30344  _cohost_broadcast
 30311-30315  _cohost_cfg
 30370-30382  _cohost_fire_highlight
 30318-30326  _cohost_gate
 30347-30367  _cohost_highlight
 29461-29495  _community_events_loop
 11106-11142  _conv_add_message
 11145-11150  _conv_archive
 11081-11090  _conv_create
 11095-11103  _conv_messages
 11153-11160  _conv_rename
  7258-7298   _cookie_alarm_loop
  1773-1777   _cookie_autorefresh_info
  1678-1682   _cookie_header
 15136-15168  _cpu_load_snapshot
  3880-3892   _create_index_safe
 13526-13541  _creator_activity
 13582-13605  _creator_dossier_generate
 13544-13555  _creator_facts_line
 26199-26305  _crowdsec_status
 26165-26196  _crowdsec_via_lapi
 26030-26048  _cscli_bin
 26054-26067  _cscli_path
  7151-7176   _daily_summary_loop
 26085-26102  _darf_journal_lesen
 28708-28728  _db_maintenance_loop
  7123-7148   _db_vacuum_loop
 20289-20313  _detect_foreign_ad
  1278-1289   _diag_path_owner
 21675-21719  _director_finalize
 22486-22493  _director_for
 21624-21672  _director_mark
 29699-29734  _disc_automod_check
 29672-29678  _disc_state_get
 29681-29688  _disc_state_set
 26748-26761  _discord_guild_filesize_bytes
 26947-26956  _discord_invite
 29633-29669  _discord_live_thread
 21826-21838  _discord_notify
 26848-26873  _discord_ops_alert
 29531-29629  _discord_post_user
 27012-28693  _discord_run_once
 26886-26944  _discord_start
 29220-29226  _discord_stop
 26769-26771  _discord_upload_limit_label
 26764-26766  _discord_upload_limit_mb
  7179-7253   _disk_alarm_loop
 31598-31647  _disk_autoclean
 31650-31663  _disk_guard_loop
 31590-31595  _disk_pct
 24762-24765  _donations_unknown_count
 18429-18431  _drawtext_chain
 15715-15717  _dump_all_threads
 12259-12323  _enrich_proxies_with_geo
  1918-1962   _ensure_cookie_file_netscape
 26959-27009  _ensure_discord_invite
 29426-29458  _ensure_error_channel
 12502-12539  _ensure_proxy_ready
  8873-8896   _ensure_topic
   636-638    _env_int
   641-643    _env_int_range
 29498-29528  _error_channel_loop
 21870-21883  _event_webhook
 17363-17369  _evo_build_dir
 17372-17379  _evo_version
 17655-17736  _evolution_cycle
 17388-17408  _evolution_llm_note
 17739-17749  _evolution_loop
 17411-17652  _evolution_write_build
  6276-6310   _extract_file_payload
  2050-2052   _extract_urls_from_streamurl_node
 26070-26077  _f2b_sudo_hint
 21906-21908  _faster_whisper_available
 20178-20190  _fetch_ldnoobw_de
 12148-12166  _fetch_proxy_list
 22320-22348  _fetch_tiktok_room_id
   687-690    _ff_cmd
 16386-16399  _ffmpeg_version_str
 18592-18597  _find_chromium
  3021-3025   _find_external_recorder
  2055-2057   _find_stream_urls
 16314-16339  _fire_webhooks
  8034-8043   _fork_safe
   769-778    _freeai_chat_sync_metered
 26120-26162  _geo_lookup_ips
  3480-3489   _get_ai_session
  7868-7908   _get_live_info
  2591-2598   _get_resolve_semaphore
  8222-8587   _handle_single_tracking
 31442-31444  _hb
 31447-31464  _hb_while
 18130-18132  _highlight_cfg
 18135-18164  _highlight_observe
 18600-18605  _htmlov_screenshot_cmd
 22064-22074  _httpx_proxy
 16347-16359  _in_quiet_hours
 32431-32462  _install_fast_eventloop
 10158-10212  _install_fast_json
 15720-15736  _install_faulthandler
 23172-23181  _intel_ensure_schema
 23265-23296  _intel_index_loop
 23193-23203  _intel_index_one
 23184-23190  _intel_semantic
  5645-5654   _is_authorized
  8152-8158   _is_dead
  2040-2042   _is_hevc
 26105-26111  _is_private_ip
  1424-1431   _is_process_running
  6864-6875   _is_quiet_hours
  1086-1095   _is_upload_window
 10247-10260  _json_error_handler
  7081-7111   _kick_broadcaster_id
 13032-13051  _kick_channel_live
  6998-7040   _kick_follower_count
 14094-14107  _kick_oauth_exchange
 14110-14112  _kick_oauth_page
 14053-14057  _kick_redirect_public
 14044-14050  _kick_redirect_source
 14030-14041  _kick_redirect_uri
  6983-6985   _kick_slug
 14060-14091  _kick_user_token
  3929-3932   _kind_from_filename
 16376-16381  _latest_popularity
 20200-20206  _learned_load
 20197-20198  _learned_path
 20208-20216  _learned_save
 22701-22731  _live_react_loop
 22497-22690  _live_react_worker
 21287-21298  _live_transcript_push
 22692-22699  _live_users
 21722-21766  _living_title_loop
  3543-3553   _llm_list_models
 20157-20165  _load_banned_words_file
  1599-1672   _load_cookies_dict
 28901-28973  _local_backup_scan
 10229-10243  _log_5xx
 19015-19019  _looks_like_codec_err
 19010-19012  _looks_like_source_expired
  8115-8145   _loop_fehler
 15740-15749  _loop_heartbeat
 31412-31439  _loop_lag_monitor
 15859-15862  _loop_not_ready
 15752-15820  _loop_watchdog_thread
 21167-21181  _loyalty_add
 21158-21164  _loyalty_get
 21184-21192  _loyalty_top
 16760-16778  _manual_donations_rows
 16781-16783  _manual_donations_total
  8160-8161   _mark_dead
 13199-13228  _marketing_cfg
 13190-13196  _marketing_default_targets
 13185-13187  _marketing_enabled
 13242-13257  _marketing_flavor
 13312-13328  _marketing_loop
 13260-13270  _marketing_post_discord
 13273-13285  _marketing_post_telegram
 13288-13309  _marketing_publish
 13231-13235  _marketing_state_obj
 13238-13239  _marketing_state_save
 30232-30250  _maybe_handle_command
 31749-31773  _maybe_hype_clip
  3847-3870   _migrate_columns
 30507-30518  _mod_is_exempt
 30521-30526  _mod_warn_first
 30529-30532  _mod_warn_text
 17918-17926  _modlog
   890-892    _multistream_targets
  8046-8047   _nc_create_subprocess_exec
  8050-8051   _nc_create_subprocess_shell
 13423-13439  _news_cfg
 13410-13412  _news_enabled
 13477-13518  _news_facts
 13632-13654  _news_generate
 13837-13854  _news_loop
 13415-13420  _news_output_path
 13521-13523  _news_phrase
 13608-13629  _news_phrase_impl
 13452-13459  _news_read
 13442-13445  _news_state_obj
 13448-13449  _news_state_save
 13462-13474  _news_write
 25090-25114  _nl_to_sql
 17956-17958  _normalize_ingest
  2232-2249   _note_check_duration
 21313-21321  _oracle_memories
 21579-21613  _oracle_memorize
 21324-21337  _oracle_persona
 21306-21310  _oracle_recent_text
 18255-18263  _ov_atomic_write
 18243-18249  _ov_bar
 20113-20125  _ov_clip_text
 18252-18253  _ov_oneline
 24773-24802  _overlay_push
 18546-18589  _overlay_render_size
 18017-18021  _overlay_session_reset
 24721-24724  _overlay_src_ok
 20276-20286  _own_invites
 16741-16757  _parse_eur
 18541-18543  _parse_size
 26313-26393  _parse_ssh_attacks
  7470-7503   _pause_resume_cmd
  1727-1771   _persist_refreshed_cookies
  1565-1597   _pick_checked_pull_proxy
 10315-10320  _pin_auth_value
 10352-10353  _pin_clear_fail
 10332-10335  _pin_locked
 10338-10349  _pin_note_fail
 10323-10329  _pin_ok
 24611-24613  _piper_available
 24576-24598  _piper_list_voices
 24618-24643  _piper_pick_model
 24655-24702  _piper_say
 24569-24573  _piper_voice_roots
 16276-16311  _post_json_threaded
 18520-18538  _probe_video_size
  1452-1469   _proc_is_recorder
 12246-12257  _proxy_geo_cache_put
 12473-12499  _proxy_pool_refresh_loop
  1531-1562   _proxy_report_recording
 15705-15707  _prune_stall_dumps
 13657-13778  _public_stats
 21841-21867  _push_notify
 10454-10456  _pwa_dir
 12217-12232  _quick_validate_proxy
 16342-16344  _quiet_hours_config
 10419-10452  _rate_guard
 21132-21138  _react_warn
  7954-7993   _reap_proc
  2272-2294   _record_check_outcome
   682-684    _redact_stream_urls
 12400-12470  _refresh_proxy_pool
 24601-24607  _resolve_piper_model
  2066-2156   _resolve_via_html
  2414-2568   _resolve_via_webcast_api_v2
  2631-2693   _resolve_via_ytdlp
 29851-29980  _resolve_youtube_ingest
 22770-22777  _restream_active_platforms
 18002-18013  _restream_active_sources
 22351-22450  _restream_chat_guardian
 18167-18239  _restream_chat_push
 17929-17941  _restream_enabled
 18608-18695  _restream_html_overlay_start
 18698-18711  _restream_html_overlay_stop
  1034-1036   _restream_layout_mode
 17967-17990  _restream_overlay_files
 22735-22767  _restream_platform_state
 22891-22926  _restream_resume_after_restart
 18759-18817  _restream_tts_enqueue_wav
 18482-18514  _restream_tts_feeder
 18479-18480  _restream_tts_fifo_path
 18714-18741  _restream_tts_start
 18743-18757  _restream_tts_stop
 22780-22888  _restream_verify_loop
 28866-28878  _retention_loop
 28825-28863  _retention_scan
  2376-2378   _room_is_abo
  6314-6431   _run_ai_call
 15843-15856  _run_async_from_flask
 26114-26117  _run_priv
 32419-32427  _run_selfcheck_and_exit
 28881-28892  _s3_client
 25054-25085  _safe_select
  8163-8209   _safe_send
  4797-4813   _sample_net_throughput
 20167-20175  _save_banned_words_file
  2324-2351   _schedule_next_check
 28784-28822  _scheduler_loop
  3873-3877   _schema_pk
 15864-15869  _scraper_session
 30535-30574  _screen_full
 14420-14457  _sec_headers
  2045-2047   _select_stream_from_data_section
 32232-32416  _selfcheck
  1109-1113   _should_defer_upload
 29292-29327  _shrink_for_discord
 31670-31687  _sign_health_check
 31690-31709  _sign_health_loop
  8063-8074   _spawn
  8077-8107   _spawn_from_flask
 26437-26440  _st_befund
 22076-22317  _start_chat_listener
 15823-15840  _start_loop_watchdog
 13802-13828  _stats_loop
 13781-13784  _stats_output_path
 13787-13799  _stats_write
  8655-8669   _storage_cleanup_loop
 31729-31736  _story_for
  3083-3089   _stream_url_expiry
  3098-3104   _stream_url_is_fresh
  3091-3096   _stream_url_ttl
 20240-20247  _streamer_persona_get
 20222-20228  _streamer_personas_load
 20219-20220  _streamer_personas_path
 20230-20238  _streamer_personas_save
 18434-18438  _studio_chain
 28998-29120  _system_backup
 29123-29151  _system_backup_loop
 12169-12208  _test_proxy
 13073-13082  _testpush_cfg
 13085-13102  _testpush_exec
 13054-13070  _testpush_resolve_live
  8832-8842   _tg_topics_load_into_mem
  8829-8830   _tg_topics_path
  8844-8851   _tg_topics_save
 25647-25695  _tiktok_account_exists
 10298-10306  _token_ok
  8854-8858   _topic_forget
 16362-16373  _tracking_max_duration
  1336-1359   _try_attach_file_handler
 24645-24653  _tts_cleanup
 12958-12961  _tunnel_effective
 24071-24124  _twitch_channel_status
 30577-30719  _twitch_chat_loop
 30393-30494  _twitch_eventsub_loop
 17181-17184  _twitch_oauth_page
  1132-1145   _upload_queue_add
  1156-1158   _upload_queue_count
  1115-1124   _upload_queue_load
  1105-1107   _upload_queue_path
  1147-1154   _upload_queue_remove
  1126-1130   _upload_queue_save
  1160-1198   _upload_window_loop
  7927-7934   _uptime_s
 17944-17953  _url_host
   747-751    _usage_record_claude
  7043-7071   _viewer_sample_loop
  7113-7120   _viewer_stats
 10356-10359  _wants_html
  7937-7951   _warn_empty_env
 31485-31580  _watchdog_loop
 30134-30142  _wchat_thank_ok
 21910-21940  _whisper_get_model
  8024-8031   _whisper_native_section
 21119-21125  _whisper_pool
 22009-22038  _whisper_segments
 21942-22006  _whisper_transcribe
 18265-18427  _write_restream_overlay
 30747-30820  _youtube_api_chat_loop
 24127-24230  _youtube_api_status
 24233-24300  _youtube_channel_status
 30823-30980  _youtube_chat_loop
 29986-29999  _youtube_restream_autoconfig
 30002-30026  _youtube_restream_autoconfig_inner
 30092-30120  _youtube_send
 24405-24446  _youtube_set_channel
 30029-30063  _yt_access_token
 30066-30081  _yt_live_chat_id
 30740-30744  _yt_oauth_configured
 30087-30089  _yt_sendrate_cfg
 30722-30737  _yt_timeout
  2615-2616   _ytdlp_detect_available
  2618-2629   _ytdlp_note_result
 15710-15712  _zombie_child_count
  7804-7828   about
  4048-4067   add_ai_log_entry
  3965-3968   add_archive_entry
  4910-4925   add_archive_rule
  4492-4526   add_recording
  4153-4170   add_tracking
  4587-4604   add_tracking_tag
  6434-6467   ai
  3712-3751   ai_chat
  3785-3795   ai_history_append
  3797-3802   ai_history_clear
  3774-3783   ai_history_load
  3759-3772   ai_rate_limit_check
  6496-6504   aireset
 21450-21469  azrael_chat
 30985-31107  brain_cmd
  3107-3291   build_recording_cmd
  4173-4250   bulk_add_trackings
  7301-7360   bulkadd
  8672-8812   check_all_trackings
  4337-4349   claim_live_transition
 20316-21062  class KickModerator
 19022-20000  class RestreamManager
 12584-12626  classify_proxy_anonymity
  6542-6740   cleanup
  5505-5546   cleanup_old_recordings
  4483-4490   clear_recording
 29737-29802  clip_moment
  5058-5101   cluster_failures
  4741-4790   compute_storage_forecast
  7423-7467   cookies_cmd
  5347-5353   cookies_days_old
  4144-4150   count_trackings_for_chat
  4035-4046   decide_preferred_recorder
  3975-3978   delete_archive_entry
  4927-4935   delete_archive_rule
  5971-6118   diag
 31110-31171  einnahmen_cmd
  4735-4738   find_recordings_by_fingerprint
  3996-4012   finish_recording_attempt
  4282-4292   get_all_active_trackings
  4089-4092   get_all_checks
  4528-4531   get_all_recordings
  4629-4639   get_all_tags_with_counts
  4712-4715   get_annotations_for_recording
  3970-3973   get_archive_entry
  4705-4708   get_bookmarked_recordings
  1794-1911   get_cookie_health
  4578-4584   get_event_log
  4019-4033   get_last_recording_attempt
  2696-2801   get_live_status
  5261-5264   get_manual_recordings
  4720-4723   get_or_compute_inspect_sync
  5581-5625   get_outcome_breakdown
  4686-4694   get_priority_poll_interval
  4888-4897   get_profile_snapshots
  4069-4079   get_recent_ai_log
  4014-4017   get_recent_recording_attempts
  4533-4536   get_recording_by_id
  4698-4701   get_recording_note
  3428-3451   get_redis
  4120-4136   get_stats
  5472-5503   get_storage_stats
  4619-4627   get_tags_for_tracking
  5028-5042   get_tiktok_status_distribution
  4673-4684   get_tracking_priority
  4351-4360   get_tracking_state
  4278-4280   get_trackings_for_group
  5277-5280   get_trash_recordings
  9516-10126  handle_recording_finished
  3895-3920   init_db
  5395-5449   inspect_stream_url
 24768-24770  is_revenue_platform
  4900-4908   list_archive_rules
  5775-5813   live
  8212-8220   live_check_worker
  3503-3537   llm_chat
  3602-3669   llm_chat_stream_sync
  3571-3599   llm_chat_sync
  3556-3568   llm_list_models
  4544-4570   log_event
  1386-1419   log_recording_failure
  7617-7666   logs_cmd
 31777-32222  main
  6470-6493   on_ai_media
  7743-7769   on_ai_reply
  7772-7801   on_azrael_mention
  7833-7863   on_callback
 21472-21576  oracle_handle
  7506-7509   pause_tracking
  5635-5640   profile_keyboard
  5356-5392   quick_restart_tracking
  7568-7614   quota
  8589-8652   reaper_loop
  5024-5026   record_tiktok_status
  6509-6539   recstatus
  3453-3461   redis_get_json
  3463-3469   redis_set_json
  4252-4276   remove_tracking
  4606-4617   remove_tracking_tag
 31174-31184  report_cmd
 12629-12631  report_proxy_result
  2159-2186   resolve_tiktok_live_stream
  5272-5275   restore_recording
  7512-7515   resume_tracking
  4938-5018   run_archive_rules
 31187-31392  run_bot
 15632-15679  run_flask
  4816-4861   sample_bandwidth_for_active
  4867-4886   save_profile_snapshot
  4081-4087   save_tiktok_check
  4475-4481   set_recording_file
  4295-4333   set_tracking_paused
  4642-4671   set_tracking_priority
  5267-5270   soft_delete_recording
  8901-9514   split_and_send_video
  5688-5730   start
  3980-3994   start_recording_attempt
  6743-6781   stats
  5242-5259   stop_manual_recording
  7518-7565   stoprec
  6968-6976   summary_cmd
  7669-7740   sysres
  6120-6264   teststream
  5732-5773   tiktok
  7363-7420   topusers
  5850-5907   track
  5815-5847   track_exact
  5921-5969   tracklist
  5108-5240   trigger_manual_recording
  4436-4473   try_acquire_recording_lock
  5283-5342   universal_search
  5909-5919   untrack
  4730-4733   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
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
